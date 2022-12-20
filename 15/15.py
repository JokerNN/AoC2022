from dataclasses import dataclass
import re
from typing import List, Generator
from utils.inputs import get_input_lines
from utils.geometry import Point
# from PIL import Image, ImageDraw

parsing_re = re.compile(r'Sensor at x=(?P<sensor_x>\-?\d+), y=(?P<sensor_y>\-?\d+): closest beacon is at x=(?P<beacon_x>\-?\d+), y=(?P<beacon_y>\-?\d+)') #pylint: disable=line-too-long

@dataclass(frozen=True)
class Sensor:
    pos: Point
    beacon: Point
    dist: int

def calc_manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_manhattan_circle(p: Point, radius: int) -> Generator[Point, None, None]:
    top = Point(p.x, p.y - radius)
    right = Point(p.x + radius, p.y)
    bottom = Point(p.x, p.y + radius)
    left = Point(p.x - radius, p.y)
    cur_point = top
    while cur_point != right:
        yield cur_point
        cur_point = Point(cur_point.x + 1, cur_point.y + 1)

    while cur_point != bottom:
        yield cur_point
        cur_point = Point(cur_point.x - 1, cur_point.y + 1)

    while cur_point != left:
        yield cur_point
        cur_point = Point(cur_point.x - 1, cur_point.y - 1)

    while cur_point != top:
        yield cur_point
        cur_point = Point(cur_point.x + 1, cur_point.y - 1)


def main():
    test_row = 2_000_000
    # test_row = 10
    sensors: List[Sensor] = []
    for line in get_input_lines('./input.txt'):
        m = parsing_re.match(line)
        if m is None:
            raise Exception('Parsing error')

        sensor_x = int(m.group('sensor_x'))
        sensor_y = int(m.group('sensor_y'))
        beacon_x = int(m.group('beacon_x'))
        beacon_y = int(m.group('beacon_y'))

        sensor_pos = Point(sensor_x, sensor_y)
        beacon_pos = Point(beacon_x, beacon_y)
        sensor = Sensor(sensor_pos, beacon_pos, calc_manhattan_distance(sensor_pos, beacon_pos))
        sensors.append(sensor)

    count = 0
    for x in range(-6_000_000, 6_000_000):
    # for x in range(-100, 100):
        if x % 100000 == 0:
            print(x)

        test_p = Point(x, test_row)
        for sensor in sensors:
            if calc_manhattan_distance(test_p, sensor.pos) <= sensor.dist and \
                    test_p != sensor.beacon:

                count += 1
                break

    print(f'Answer 1: {count}')
    # print(f'Answer 1: 5299855')
    # print(Image)
    # img = Image.new('1', (2500, 1200), color=1)
    # # img.putpixel((0, 0), 0)
    # draw = ImageDraw.Draw(img)
    # for sensor in sensors:
    #     offset = 2
    #     top = (sensor.pos.x // 5000, (sensor.pos.y - sensor.dist) // 5000 + offset)
    #     right = ((sensor.pos.x + sensor.dist) // 5000 - offset, sensor.pos.y // 5000)
    #     bottom = (sensor.pos.x // 5000, (sensor.pos.y + sensor.dist) // 5000 - offset)
    #     left = ((sensor.pos.x - sensor.dist) // 5000 + offset, sensor.pos.y // 5000)
    #     draw.polygon([top, right, bottom, left], fill=0, outline=None)
    #     top_left = (sensor.pos.x // 5000 - 5, sensor.pos.y // 5000 - 5)
    #     bottom_right = (sensor.pos.x // 5000 + 5, sensor.pos.y // 5000 + 5)
    #     draw.arc([top_left, bottom_right], 0, 360, fill=0, width=6)

    # border = 4_000_000 // 5000
    # draw.line([(border, 0), (border, border)], fill=0, width=5)
    # draw.line([(0, border), (border, border)], fill=0, width=5)
    # img.save('/Users/ataktaev/Documents/AoC2022/tst.png')

    # # find search area visually
    # sa_x = 516 * 5000
    # sa_y = 730 * 5000
    # for x in range(515 * 5000, 517 * 5000):
    #     if x % 1000 == 0:
    #         print(x)
    #     for y in range(729 * 5000, 731 * 5000):
    #         p = Point(x, y)
    #         for sensor in sensors:
    #             if calc_manhattan_distance(p, sensor.pos) <= sensor.dist:
    #                 break
    #         else:
    #             print('found', p)
    search_area = 20
    search_area = 4_000_000
    res: Point = Point(0, 0)
    for sensor in sensors:
        if res != Point(0, 0):
            break
        # print(sensor)
        for point in get_manhattan_circle(sensor.pos, sensor.dist + 1):
            if point.x < 0 or point.x > search_area or point.y < 0 or point.y > search_area:
                continue
            for sensor_inner in sensors:
                if calc_manhattan_distance(point, sensor_inner.pos) <= sensor_inner.dist:
                    break
            else:
                if 0 <= point.x <= search_area and 0 <= point.y <= search_area:
                    res = point
                    print(f'Found: {point}')
                    break

    print(f'Answer 2: {res.x * 4_000_000 + res.y}')

if __name__ == '__main__':
    main()
