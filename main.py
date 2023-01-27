import sys
from logClass import Log, line_analysis

def init_Log_from_igc(igc_file):
    with open(igc_file) as f:
        lines = f.readlines()
    metadata = []
    logs = []
    for i, line in enumerate(lines):
        if line[0] != "B":
            metadata.append(line)
        else:
            logs.append(line_analysis(line))
    return Log(logs, metadata)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception('python3 main.py igc_file')
    
    igc_file = sys.argv[1]
    log_data = init_Log_from_igc(igc_file)
    log_data.print_stats()