import pandas as pd

class ExcelExporter:
    @staticmethod
    def export_to_excel(scan_results, file_path):
        try:
            df = pd.DataFrame(scan_results, columns=["Porta", "Protocollo", "Tipo Protocollo", "Stato"])
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Scansione')
                worksheet = writer.sheets['Scansione']
                worksheet.add_table('A1:D{}'.format(len(df) + 1), {'columns': [{'header': col} for col in df.columns]})
            return f"Risultati esportati in {file_path}"
        except Exception as e:
            return f"Errore durante l'esportazione: {e}"