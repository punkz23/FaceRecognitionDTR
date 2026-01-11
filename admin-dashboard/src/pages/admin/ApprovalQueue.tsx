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
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  
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

  const openReviewModal = (user: User) => {
    setSelectedUser(user);
    setEditName(user.full_name);
    setEditId(user.employee_id);
    setSelectedBranch("");
    setRejectionReason("");
    setIsReviewOpen(true);
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
        setIsReviewOpen(false);
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
        setIsReviewOpen(false);
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
                    <div className="flex items-center space-x-4">
                      <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center overflow-hidden border-2 border-muted hover:border-primary transition-all hover:scale-105">
                        {user.face_image_url ? (
                          <img 
                            src={user.face_image_url.trim()} 
                            alt={user.full_name} 
                            className="h-full w-full object-cover"
                            onError={(e) => {
                              console.error("Image load failed for:", user.face_image_url);
                              (e.target as HTMLImageElement).style.display = 'none';
                              // This will show the background/fallback if image fails
                            }}
                          />
                        ) : (
                          <UserIcon className="h-8 w-8 text-muted-foreground" />
                        )}
                      </div>
                      <div className="font-medium text-lg">{user.full_name}</div>
                    </div>
                  </TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono">
                      {user.employee_id}
                    </code>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="text-blue-600 border-blue-200 hover:bg-blue-50 px-4"
                      onClick={() => openReviewModal(user)}
                    >
                      <UserIcon className="h-4 w-4 mr-2" />
                      Review & Approve
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Unified Review Modal */}
      <Dialog open={isReviewOpen} onOpenChange={setIsReviewOpen}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle className="text-2xl">Review Employee Registration</DialogTitle>
            <DialogDescription>
              Verify the employee's identity and assign a branch for approval.
            </DialogDescription>
          </DialogHeader>
          
          <div className="max-h-[70vh] overflow-y-auto px-1">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 py-6">
              {/* Left Column: Large Photo */}
              <div className="flex flex-col items-center justify-center space-y-4 bg-muted/30 p-4 rounded-xl border border-dashed">
                <span className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Captured Face</span>
                {selectedUser?.face_image_url ? (
                  <div className="relative group">
                    <img 
                      src={selectedUser.face_image_url} 
                      alt="Enrolled Face" 
                      className="w-80 h-80 object-cover rounded-2xl border-4 border-white shadow-2xl transition-transform group-hover:scale-[1.02]"
                    />
                    <div className="absolute inset-0 rounded-2xl ring-1 ring-inset ring-black/10"></div>
                  </div>
                ) : (
                  <div className="w-80 h-80 bg-muted flex items-center justify-center rounded-2xl border-4 border-white shadow-inner">
                    <UserIcon className="h-32 w-32 text-muted-foreground/40" />
                  </div>
                )}
              </div>

              {/* Right Column: Details */}
              <div className="flex flex-col space-y-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-bold border-b pb-2">Employee Details</h3>
                  
                  <div className="grid gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="rev-name" className="font-semibold text-muted-foreground">Full Name</Label>
                      <Input 
                        id="rev-name" 
                        value={editName} 
                        onChange={(e) => setEditName(e.target.value)}
                        className="text-lg h-11"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label htmlFor="rev-id" className="font-semibold text-muted-foreground">Employee ID</Label>
                        <Input 
                          id="rev-id" 
                          value={editEmpId} 
                          onChange={(e) => setEditId(e.target.value)}
                          className="font-mono"
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="rev-email" className="font-semibold text-muted-foreground">Email Address</Label>
                        <Input 
                          id="rev-email" 
                          value={selectedUser?.email || ""} 
                          disabled
                          className="bg-muted/50"
                        />
                      </div>
                    </div>

                    <div className="grid gap-2">
                      <Label htmlFor="rev-branch" className="font-bold text-primary">Assigned Branch (Required for Approval)</Label>
                      <select 
                        id="rev-branch"
                        className="flex h-11 w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
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
                </div>

                <div className="space-y-4 pt-4 border-t">
                  <h3 className="text-lg font-bold text-red-600">Rejection Details</h3>
                  <div className="grid gap-2">
                    <Label htmlFor="rev-reason" className="font-semibold text-muted-foreground">Reason for Disapproval</Label>
                    <textarea 
                      id="rev-reason"
                      className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                      placeholder="Provide a clear reason if you are rejecting this application..."
                      value={rejectionReason}
                      onChange={(e) => setRejectionReason(e.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <DialogFooter className="gap-4 sm:justify-between border-t pt-6">
            <Button 
              variant="outline" 
              onClick={() => setIsReviewOpen(false)}
              className="px-8"
            >
              Cancel
            </Button>
            <div className="flex gap-4 w-full sm:w-auto">
              <Button 
                variant="destructive"
                className="flex-1 sm:px-12 h-12 text-lg font-bold shadow-lg shadow-red-200"
                onClick={handleReject}
              >
                <X className="h-5 w-5 mr-2" />
                Disapprove
              </Button>
              <Button 
                className="flex-1 sm:px-12 h-12 text-lg font-bold bg-green-600 hover:bg-green-700 shadow-lg shadow-green-200"
                onClick={handleApprove}
              >
                <Check className="h-5 w-5 mr-2" />
                Approve Employee
              </Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
