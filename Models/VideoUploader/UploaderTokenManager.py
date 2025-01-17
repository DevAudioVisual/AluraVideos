def token():
    from Config import LoadConfigs
    return LoadConfigs.Config.getConfigData(config="Credentials",data="VideoUploaderToken")
