

def read_inf(path):
    header = {}
    data = {}
    header_ = True
    data_header_flag = 0
    data_header = ''
    with open(path) as f:
        for line in f.readline():
            if len(line) == 0:
                continue
            if header_:
                split_line = line.split(':')
                if len(split_line) == 0:
                    pass
                if len(split_line) == 1:
                    key, value = split_line[0], None
                elif len(split_line) == 2:
                    key, value = split_line[0], split_line[1]
                else:
                    key, value = split_line[0], ', '.join(split_line[1:])
                header[key] = value
                if key == 'PRESSURE DATA':
                    header_ = False
            else:
                if line.count('-') == len(line.strip()):
                    if data_header_flag == 0:
                        data_header_flag = 1
                    elif data_header_flag == 1:
                        data_header_flag = 2
                    continue
                if data_header_flag == 1:
                    data_header = data_header + line
                if data_header_flag == 2:
                    data_header_flag = 3

                    data_header = [l for l in line.split('  ') if len(l.split()) > 0]
