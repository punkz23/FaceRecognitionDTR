import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Check, X, RefreshCw, User as UserIcon } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface User {
  id: string;
  full_name: string;
  email: string;
  status: string;
  employee_id: string;
  face_image_url?: string;
}

interface Branch {
  id: number;
  name: string;
}

export default function ApprovalQueue() {
  const [users, setUsers] = useState<User[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Modals state
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isApproveOpen, setIsApproveOpen] = useState(false);
  const [isRejectOpen, setIsRejectOpen] = useState(false);
  
  // Form state
  const [editName, setEditName] = useState("");
  const [editEmpId, setEditId] = useState("");
  const [selectedBranchId, setSelectedBranch] = useState<string>("");
  const [rejectionReason, setRejectionReason] = useState("");

  const getHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };
  };

  const fetchPendingUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/users/', {
        headers: getHeaders(),
      });
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

  const fetchBranches = async () => {
    try {
      const response = await fetch('/api/v1/branches/', {
        headers: getHeaders(),
      });
      if (response.ok) {
        const data = await response.json();
        setBranches(data);
      }
    } catch (error) {
      console.error("Failed to fetch branches", error);
    }
  };

  useEffect(() => {
    fetchPendingUsers();
    fetchBranches();
  }, []);

  const openApproveModal = (user: User) => {
    setSelectedUser(user);
    setEditName(user.full_name);
    setEditId(user.employee_id);
    setSelectedBranch("");
    setIsApproveOpen(true);
  };

  const openRejectModal = (user: User) => {
    setSelectedUser(user);
    setRejectionReason("");
    setIsRejectOpen(true);
  };

  const handleApprove = async () => {
    if (!selectedUser) return;
    if (!selectedBranchId) {
      alert("Please select a branch.");
      return;
    }

    try {
      const response = await fetch(`/api/v1/admin/users/${selectedUser.id}/status`, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({ 
          status: 'APPROVED',
          branch_id: parseInt(selectedBranchId),
          full_name: editName,
          employee_id: editEmpId
        }),
      });

      if (response.ok) {
        setUsers(users.filter(u => u.id !== selectedUser.id));
        setIsApproveOpen(false);
      } else {
        const error = await response.json();
        alert(error.detail || "Failed to approve user");
      }
    } catch (error) {
      console.error("Error approving user", error);
    }
  };

  const handleReject = async () => {
    if (!selectedUser) return;
    if (!rejectionReason) {
      alert("Please provide a rejection reason.");
      return;
    }

    try {
      const response = await fetch(`/api/v1/admin/users/${selectedUser.id}/status`, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({ 
          status: 'REJECTED',
          rejection_reason: rejectionReason
        }),
      });

      if (response.ok) {
        setUsers(users.filter(u => u.id !== selectedUser.id));
        setIsRejectOpen(false);
      } else {
        const error = await response.json();
        alert(error.detail || "Failed to reject user");
      }
    } catch (error) {
      console.error("Error rejecting user", error);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Pending Registrations</h2>
          <p className="text-sm text-muted-foreground">Review and approve new employee accounts.</p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchPendingUsers} disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Contact</TableHead>
              <TableHead>Employee ID</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center h-24 text-muted-foreground">
                  {loading ? "Loading..." : "No pending registrations found."}
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>
                    <div className="flex items-center space-x-3">
                      <div className="h-10 w-10 rounded-full bg-muted flex items-center justify-center">
                        <UserIcon className="h-6 w-6 text-muted-foreground" />
                      </div>
                      <div className="font-medium">{user.full_name}</div>
                    </div>
                  </TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono">
                      {user.employee_id}
                    </code>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="text-green-600 border-green-200 hover:bg-green-50"
                      onClick={() => openApproveModal(user)}
                    >
                      <Check className="h-4 w-4 mr-1" />
                      Review & Approve
                    </Button>
                    <Button 
                      size="sm" 
                      variant="ghost" 
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      onClick={() => openRejectModal(user)}
                      aria-label="Reject"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Approve Modal */}
      <Dialog open={isApproveOpen} onOpenChange={setIsApproveOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Approve Registration</DialogTitle>
            <DialogDescription>
              Assign a branch to activate this employee account.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            {selectedUser?.face_image_url && (
              <div className="flex justify-center mb-4">
                <img 
                  src={selectedUser.face_image_url} 
                  alt="Enrolled Face" 
                  className="w-32 h-32 object-cover rounded-full border-2 border-primary"
                />
              </div>
            )}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="app-name" className="text-right">Full Name</Label>
              <Input 
                id="app-name" 
                value={editName} 
                onChange={(e) => setEditName(e.target.value)}
                className="col-span-3" 
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="app-id" className="text-right">Emp ID</Label>
              <Input 
                id="app-id" 
                value={editEmpId} 
                onChange={(e) => setEditId(e.target.value)}
                className="col-span-3" 
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="branch" className="text-right font-bold text-primary">Assign Branch</Label>
              <select 
                id="branch"
                className="col-span-3 flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                value={selectedBranchId}
                onChange={(e) => setSelectedBranch(e.target.value)}
              >
                <option value="">Select a branch...</option>
                {branches.map(b => (
                  <option key={b.id} value={b.id}>{b.name}</option>
                ))}
              </select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsApproveOpen(false)}>Cancel</Button>
            <Button className="bg-green-600 hover:bg-green-700" onClick={handleApprove}>
              Complete Approval
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Reject Modal */}
      <Dialog open={isRejectOpen} onOpenChange={setIsRejectOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-red-600">Reject Registration</DialogTitle>
            <DialogDescription>
              Please provide a reason for rejecting this registration. This will be sent to the user.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="reason">Rejection Reason</Label>
              <textarea 
                id="reason"
                className="flex min-h-[80px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                placeholder="e.g. Profile picture is not clear."
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsRejectOpen(false)}>Cancel</Button>
            <Button variant="destructive" onClick={handleReject}>
              Reject Registration
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
