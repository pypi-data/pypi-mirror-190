import subprocess
import pandas as pd
import os
import random


def run_os_level_command(command, switch_sudo_user=False):
    """ This function calls os level command"""
    shell_type = ["sudo", "bash", "-c", command] if switch_sudo_user else ["sh", "-c", command]
    output = subprocess.run(shell_type, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
    if output.returncode != 0:
        print(output)
        return False
    return True


def verify_credentials(username, password):
    """Verify credentials"""
    command = "echo '{1}' | kinit {0}".format(username, password)
    is_valid_credentials = run_os_level_command(command)
    return is_valid_credentials


# def copy_kdm_artifact(kdm_directory, kdm_filename):
#     """Generate ticket for kerberos"""
#     command = "sudo cp {0}/{1} /etc/".format(kdm_directory, kdm_filename)
#     is_valid_ticket = run_os_level_command(command)
#     return is_valid_ticket


def create_new_host(kerberos_service_ip, host_name):
    """Copy KERBEROS_SERVICE_IP in hosts file"""
    command = "sudo su; sudo echo '{0} {1}' >> /etc/hosts;".format(kerberos_service_ip, host_name)
    switch_sudo_user = True
    is_file_copied = run_os_level_command(command, switch_sudo_user)
    return is_file_copied


def read_hive_configuration(kdm_directory, hive_config_file):
    """ read hive connection details"""
    df = pd.read_json(r"{0}/{1}".format(kdm_directory, hive_config_file), typ='series')
    return df.to_dict()


def set_environment_value(var_name, var_value):
    """export variable"""
    os.environ[var_name] = var_value


def get_ads_data(sql_query, database_name, username, password,
                 kdm_directory='/etc', hive_config_file='hive_config.json', row_size=None, source='hive',
                 compress=False):
    """
    This function generates auth ticket and returns result in dataframe
    arguments it accepts
    sql_query : operation to be performed specified by sql_query
    database_name: database to connect
    username: username of kerberos
    password: password of kerberos
    kdm_directory : default directory location of kdc file is /data,
    you can specify other location
    kdm_filename: default kdc file name is krb5.conf,
    you can specify other filename
    row_size : number of records to fetch, default value is 500000
    """

    # Generate principle
    is_valid_credentials = verify_credentials(username, password)
    hive_config = read_hive_configuration(kdm_directory, hive_config_file)
    #is_host_appended = create_new_host(hive_config.get("KERBEROS_SERVICE_IP"),
    #                            hive_config.get("KEREROS_SERVICE_ALIAS"))

    if is_valid_credentials and hive_config:
        conn = get_hive_connection(hive_config, source, database_name)
        conn.execute(sql_query)
        df = pd.DataFrame()
        row_size = 500000 if row_size is None else row_size
        data = conn.fetchmany(row_size)
        field_names = [i[0] for i in conn.description]
        while data:
            df1 = pd.DataFrame(data, columns=field_names)
            if compress:
                df1 = squeeze_dataframe(df1)
            df = pd.concat([df, df1])
            del df1
            data = conn.fetchmany(row_size)
        return df


def get_hive_connection(hive_config, source, database_name):
    """
    Get hive connection cursor based on source type
    :param hive_config: dict having hive configuration
    :param source: create hive connection directly to hive host or get hive connection details from zookeeper
    :param database_name: hive database name
    :return: hive connection cursor
    """
    from pyhive import hive
    if source == "hive":
        # set KEREROS_SERVICE_ALIAS in environment variable, will be used by pyhive library
        set_environment_value('HIVE_HOSTNAME', hive_config.get("KEREROS_SERVICE_ALIAS"))
        return hive.connect(host=hive_config.get("KEREROS_SERVICE_ALIAS"),
                            port=int(hive_config.get("KERBEROS_PORT")),
                            auth=hive_config.get("KERBEROS_AUTH"),
                            kerberos_service_name=hive_config.get("KERBEROS_SERVICE_NAME"),
                            username=hive_config.get("KERBEROS_HIVE_USERNAME"),
                            scheme=hive_config.get("KERBEROS_HTTP_SCHEME"),
                            database=database_name).cursor()
    elif source == "zookeeper":
        zookeeper_host = hive_config.get("ZOOKEEPER_HOST")
        zookeeper_namespace = hive_config.get("ZOOKEEPER_NAMESPACE")
        host_list = get_host_list(zookeeper_host, zookeeper_namespace)
        host_length = host_list.__len__()
        random.seed()
        is_connected = False
        while is_connected is False and host_length > 0:
            index = random.randint(0, host_length - 1)
            host_details = host_list.pop(index)
            host = host_details.split(":")[0]
            port = host_details.split(":")[1]
            try:
                # set KEREROS_SERVICE_ALIAS in environment variable, will be used by pyhive library
                set_environment_value('HIVE_HOSTNAME', host)
                cursor = hive.connect(host=host,
                                      port=port,
                                      auth=hive_config.get("KERBEROS_AUTH"),
                                      kerberos_service_name=hive_config.get("KERBEROS_SERVICE_NAME"),
                                      username=hive_config.get("KERBEROS_HIVE_USERNAME"),
                                      scheme=hive_config.get("KERBEROS_HTTP_SCHEME"),
                                      database=database_name
                                      ).cursor()
                is_connected = True
            except Exception:
                is_connected = False
                if host_length > 1:
                    print(
                        "Can not connect " + host + ":" + port + " .try another server...")
                else:
                    print(
                        "Can not connect " + host + ":" + port + ", please check the connection config and the hiveserver")
                    raise Exception
            host_length -= 1
        return cursor


def get_host_list(host, namespace):
    """
    Get host list from zookeeper
    :param host: zookeeper URI
    :param namespace: zookeeper namespace
    :return: list of connection strings from that namespace
    """
    from kazoo.client import KazooClient
    from kazoo.handlers.threading import KazooTimeoutError
    try:
        client = KazooClient(hosts=host)
        client.start()
        node_children = client.get_children(namespace)
        host_list = []
        for hiveserver in node_children:
            server_string = hiveserver.split(';')[0].split('=')[1]
            host_list.append(server_string)
        client.stop()
        if len(host_list) == 0:
            raise Exception("No hive instance present in this zookeeper namespace")
        return host_list
    except KazooTimeoutError:
        print("Not able to connect to zookeeper server")
        raise
    except Exception as ex:
        print(ex)
        raise


def squeeze_dataframe(df):
    """
    Squeeze dataframe by reducing datatype to minimum
    :param df: dataframe to be squeeze
    :type df: pandas dataframe
    :return: squeezed dataframe
    :rtype: pandas dataframe
    """
    from pandas.api.types import CategoricalDtype
    cols = dict(df.dtypes)
    # ----- Check each column's type downcast or categorize as appropriate
    for col, type in cols.items():
        if type == 'float64':
            df[col] = pd.to_numeric(df[col], downcast='float')
        elif type == 'int64':
            df[col] = pd.to_numeric(df[col], downcast='integer')
        elif type == 'object':
            df[col] = df[col].astype(CategoricalDtype(ordered=True))
    return df
