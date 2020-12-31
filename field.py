from ingrex import Intel, utils


def main():
    """main function"""
    field = {
        "minLng": 166.071535,
        "maxLng": 166.793004,
        "minLat": 39.741368,
        "maxLat": 40.175495,
    }
    min_x_tile, max_y_tile = utils.calc_tile(field["minLng"], field["minLat"], 15)
    max_x_tile, min_y_tile = utils.calc_tile(field["maxLng"], field["maxLat"], 15)
    for x_tile in range(min_x_tile, max_x_tile + 1):
        for y_tile in range(min_y_tile, max_y_tile + 1):
            tile_key = "15_{}_{}_8_8_25".format(x_tile, y_tile)
            intel = Intel(sessionid="")
            result = intel.fetch_map([tile_key])
            entities = result["map"][tile_key]["gameEntities"]
            for entity in entities:
                if entity[0].endswith(".9"):
                    print(entity)


if __name__ == "__main__":
    main()
