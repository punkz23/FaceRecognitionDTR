import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { RefreshCw, MapPin, MapPinOff, Clock } from "lucide-react";

interface AttendanceLog {
  id: string;
  user_id: string;
  full_name?: string; // May be joined from User
  type: 'TIME_IN' | 'TIME_OUT';
  timestamp: string;
  location_verified: boolean;
  confidence_score: number;
}

export default function DTRDashboard() {
  const [logs, setLogs] = useState<AttendanceLog[]>([]);
  const [loading, setLoading] = useState(true);

  const getHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };
  };

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/admin/attendance', { // Changed endpoint
        headers: getHeaders(),
      }); 
      if (response.ok) {
        const data = await response.json();
        setLogs(data);
      }
    } catch (error) {
      console.error("Failed to fetch logs", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Attendance Monitoring</h2>
        <Button variant="outline" size="sm" onClick={fetchLogs} disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Time</TableHead>
              <TableHead>Location</TableHead>
              <TableHead>Confidence</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {logs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center h-24 text-muted-foreground">
                  {loading ? "Loading..." : "No attendance logs found."}
                </TableCell>
              </TableRow>
            ) : (
              logs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell className="font-medium">{log.full_name}</TableCell> {/* Removed || 'System User' */}
                  <TableCell>
                    <Badge variant={log.type === 'TIME_IN' ? 'default' : 'secondary'}>
                      {log.type}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center text-sm">
                      <Clock className="h-3 w-3 mr-1 text-muted-foreground" />
                      {new Date(log.timestamp).toLocaleString()}
                    </div>
                  </TableCell>
                  <TableCell>
                    {log.location_verified ? (
                      <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">
                        <MapPin className="h-3 w-3 mr-1" />
                        Verified
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="text-red-600 border-red-200 bg-red-50">
                        <MapPinOff className="h-3 w-3 mr-1" />
                        Outside
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <span className={`text-sm font-medium ${log.confidence_score > 0.9 ? 'text-green-600' : 'text-yellow-600'}`}>
                      {(log.confidence_score * 100).toFixed(1)}%
                    </span>
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
