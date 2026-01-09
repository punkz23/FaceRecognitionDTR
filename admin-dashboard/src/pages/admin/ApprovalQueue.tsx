import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Check, X, RefreshCw } from "lucide-react";

interface User {
  id: string;
  full_name: string;
  email: string;
  status: string;
  employee_id: string;
}

export default function ApprovalQueue() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPendingUsers = async () => {
    setLoading(true);
    try {
      // In a real app, we'd filter by status=PENDING on the backend
      const response = await fetch('/api/v1/users/');
      if (response.ok) {
        const data = await response.json();
        setUsers(data.filter((u: User) => u.status === 'PENDING'));
      }
    } catch (error) {
      console.error("Failed to fetch users", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPendingUsers();
  }, []);

  const handleUpdateStatus = async (userId: string, newStatus: string) => {
    try {
      const response = await fetch(`/api/v1/admin/users/${userId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });
      if (response.ok) {
        setUsers(users.filter(u => u.id !== userId));
      }
    } catch (error) {
      console.error("Failed to update status", error);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Pending Registrations</h2>
        <Button variant="outline" size="sm" onClick={fetchPendingUsers} disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Employee ID</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center h-24 text-muted-foreground">
                  {loading ? "Loading..." : "No pending registrations found."}
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell className="font-medium">{user.full_name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.employee_id}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200">
                      {user.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button 
                      size="sm" 
                      variant="ghost" 
                      className="text-green-600 hover:text-green-700 hover:bg-green-50"
                      onClick={() => handleUpdateStatus(user.id, 'APPROVED')}
                    >
                      <Check className="h-4 w-4 mr-1" />
                      Approve
                    </Button>
                    <Button 
                      size="sm" 
                      variant="ghost" 
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      onClick={() => handleUpdateStatus(user.id, 'REJECTED')}
                    >
                      <X className="h-4 w-4 mr-1" />
                      Reject
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
