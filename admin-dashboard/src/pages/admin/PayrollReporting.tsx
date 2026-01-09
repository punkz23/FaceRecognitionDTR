import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { RefreshCw, Download, FileSpreadsheet, FileText } from "lucide-react";

interface PayrollSummary {
  id: string;
  full_name: string;
  total_hours: number;
  estimated_pay: number;
}

export default function PayrollReporting() {
  const [data, setData] = useState<PayrollSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPayroll = async () => {
    setLoading(true);
    try {
      // In a real implementation, this would call a dedicated payroll endpoint
      const response = await fetch('/api/v1/admin/payroll'); 
      if (response.ok) {
        const result = await response.json();
        setData(result);
      }
    } catch (error) {
      console.error("Failed to fetch payroll", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayroll();
  }, []);

  const handleExportCSV = () => {
    console.log("Exporting CSV...");
    // TODO: Implement CSV generation
  };

  const handleExportPDF = () => {
    console.log("Exporting PDF...");
    // TODO: Implement PDF generation
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Payroll & Reporting</h2>
        <div className="space-x-2">
          <Button variant="outline" size="sm" onClick={handleExportCSV}>
            <FileSpreadsheet className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
          <Button variant="outline" size="sm" onClick={handleExportPDF}>
            <FileText className="h-4 w-4 mr-2" />
            Export PDF
          </Button>
          <Button variant="outline" size="sm" onClick={fetchPayroll} disabled={loading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee Name</TableHead>
              <TableHead>Total Hours</TableHead>
              <TableHead>Estimated Pay (PHP)</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center h-24 text-muted-foreground">
                  {loading ? "Loading..." : "No payroll data available."}
                </TableCell>
              </TableRow>
            ) : (
              data.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="font-medium">{row.full_name}</TableCell>
                  <TableCell>{row.total_hours.toFixed(2)}</TableCell>
                  <TableCell>₱{row.estimated_pay.toLocaleString()}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm">
                      <Download className="h-4 w-4 mr-2" />
                      Payslip
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
