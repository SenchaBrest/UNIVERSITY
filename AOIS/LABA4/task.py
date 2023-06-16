import logging
from math import log2, ceil
from random import randint

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_tag_offset(address, block_size):
    address = "00" + bin(address)[2:]
    offset_len = ceil(log2(block_size))
    return int(address[:-offset_len], 2), int(address[-offset_len:], 2)


def create_ram(size):
    return [0] * size


def ram_read(ram, address):
    logging.info(f'Reading from RAM: address={address}')
    return ram[address]


def ram_write(ram, address, data):
    logging.info(f'Writing to RAM: address={address}, data={data}')
    ram[address] = data


def create_cache_line(block_size):
    return {'is_empty': True, 'tag': None, 'data': [None] * block_size}


def cache_line_read(cache_line, offset):
    return cache_line['data'][offset]


def cache_line_write(cache_line, tag, offset, data):
    cache_line['is_empty'] = False
    cache_line['tag'] = tag
    cache_line['data'][offset] = data


def shift(cache_lines, index):
    cache_lines[index:] = cache_lines[index + 1:] + [cache_lines[index]]


def cache_write(cache_lines, address, block_size, ram, data):
    tag, offset = get_tag_offset(address, block_size)

    for cache_line in cache_lines:
        if cache_line['is_empty']:
            cache_line_write(cache_line, tag, offset, data)
            logging.info(f'Writing to Cache: address={address}, tag={tag}, offset={offset},data={data}')
            return

    shift(cache_lines, 0)
    cache_line_write(cache_lines[-1], tag, offset, data)
    logging.info(f'Writing to Cache: address={address}, tag={tag}, offset={offset},data={data}')


def cache_access(cache_lines, address, block_size, ram):
    tag, offset = get_tag_offset(address, block_size)

    for i, cache_line in enumerate(cache_lines):
        if cache_line['data'][offset] is not None and cache_line['tag'] == tag:
            data = cache_line_read(cache_line, offset)
            shift(cache_lines, i)
            cache_line_write(cache_lines[-1], tag, offset, data)
            logging.info(f'Cache Hit: address={address}, data={data}')
            return data

    data = ram_read(ram, address)
    cache_line_write(cache_lines[-1], tag, offset, data)
    cache_write(cache_lines, address, block_size, ram, data)
    logging.info(f'Cache Miss: address={address}, data={data}')
    return data


def show_cache(cache_lines):
    for i, cache_line in enumerate(cache_lines):
        print(f"{i}, tag={cache_line['tag']}, {cache_line['data'][0]}\t{cache_line['data'][1]}")


def main():
    ram = create_ram(2048)
    cache_lines = [create_cache_line(4) for _ in range(16)]

    for i in range(50):
        ram_write(ram, i, randint(0, 50))

    while True:
        address = input("Введите адрес: ")
        try:
            address = int(address)
        except ValueError:
            show_cache(cache_lines)
        else:
            cache_access(cache_lines, address, 2, ram)


if __name__ == '__main__':
    main()
