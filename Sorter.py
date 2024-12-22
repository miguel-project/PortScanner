class Sorter:
    @staticmethod
    def sort_results(scan_results):
        open_ports = [result for result in scan_results if result[3] == "Aperta"]
        open_ports.sort(key=lambda x: x[0])
        return open_ports