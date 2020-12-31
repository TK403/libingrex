import ingrex


def main():
    """main function"""
    sessionid = ""
    intel = ingrex.Intel(sessionid)

    result = intel.fetch_msg(0, 0, 0, 0, tab='faction')
    print(result)
    result = intel.fetch_map(['17_29630_13630_0_8_100'])
    print(result)
    result = intel.fetch_portal(guid='ac8348883c8840f6a797bf9f4f22ce39.16')
    print(result)
    result = intel.fetch_score()
    print(result)
    result = intel.fetch_region(0, 0)
    print(result)
    result = intel.fetch_artifacts()
    print(result)


if __name__ == '__main__':
    main()
