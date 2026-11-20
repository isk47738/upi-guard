clean_export_func = """        function exportIncidentLog() {
            const csv = [
                "Timestamp,Type,UTR,Amount,Status",
                "Today 02:45 AM,PhonePe,432501984211,Rs. 150.00,Verified Real",
                "Today 02:50 AM,Google Pay,432501984209,Rs. 70.00,Verified Real",
                "Today 03:01 AM,SpoofApp,FP9988112233,Rs. 500.00,Blocked Fraud",
                "Today 03:15 AM,EditedPe,T241199321098,Rs. 850.00,Blocked Splicing Fraud"
            ].join("\\n");

            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `UPI_Guard_Fraud_Incident_Report_${Date.now()}.csv`;
            a.click();
        }"""

for filename in [r'd:\web devlopment baba\fake_upi_detector\fast_scanner.html', r'd:\web devlopment baba\fake_upi_detector\index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    idx = content.find("function exportIncidentLog()")
    idx_end = content.find("</script>", idx)
    
    if idx != -1 and idx_end != -1:
        # replace from idx to just before </script>
        content = content[:idx] + clean_export_func + "\n    " + content[idx_end:]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filename} successfully!")
    else:
        print(f"Could not locate exportIncidentLog in {filename}")
