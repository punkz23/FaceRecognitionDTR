import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { 
  Settings2, 
  Map, 
  RefreshCw, 
  Plus, 
  Trash2, 
  Save, 
  X as CloseIcon,
  MapPin
} from "lucide-react";
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
import MapPicker from "@/components/MapPicker";

interface Branch {
  id?: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  radius_meters: number;
}

export default function BranchManagement() {
  const [branches, setBranches] = useState<Branch[]>([]);
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isMapOpen, setIsMapOpen] = useState(false);
  const [currentBranch, setCurrentBranch] = useState<Branch | null>(null);
  const [formData, setFormData] = useState<Branch>({
    name: "",
    address: "",
    latitude: 0,
    longitude: 0,
    radius_meters: 100,
  });
  const [tempCoords, setTempCoords] = useState({ lat: 0, lng: 0 });

  const getHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };
  };

  const fetchBranches = async () => {
    setLoading(true);
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
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBranches();
  }, []);

  const openDialog = (branch: Branch | null = null) => {
    if (branch) {
      setCurrentBranch(branch);
      setFormData({ ...branch });
    } else {
      setCurrentBranch(null);
      setFormData({
        name: "",
        address: "",
        latitude: 14.5995, // Default to Manila if adding new
        longitude: 120.9842,
        radius_meters: 100,
      });
    }
    setIsDialogOpen(true);
  };

  const openMapPicker = () => {
    setTempCoords({ lat: formData.latitude, lng: formData.longitude });
    setIsMapOpen(true);
  };

  const confirmMapLocation = () => {
    setFormData({
      ...formData,
      latitude: tempCoords.lat,
      longitude: tempCoords.lng,
    });
    setIsMapOpen(false);
  };

  const handleSave = async () => {
    try {
      const url = currentBranch 
        ? `/api/v1/branches/${currentBranch.id}` 
        : '/api/v1/branches/';
      const method = currentBranch ? 'PATCH' : 'POST';

      const response = await fetch(url, {
        method,
        headers: getHeaders(),
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setIsDialogOpen(false);
        fetchBranches();
      } else {
        const error = await response.json();
        alert(error.detail || "Failed to save branch");
      }
    } catch (error) {
      console.error("Error saving branch", error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this branch?")) return;
    try {
      const response = await fetch(`/api/v1/branches/${id}`, {
        method: 'DELETE',
        headers: getHeaders(),
      });
      if (response.ok) {
        fetchBranches();
      }
    } catch (error) {
      console.error("Error deleting branch", error);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Branch Management</h2>
          <p className="text-sm text-muted-foreground">Manage physical locations and geofences.</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={fetchBranches} disabled={loading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button size="sm" onClick={() => openDialog()}>
            <Plus className="h-4 w-4 mr-2" />
            Add Branch
          </Button>
        </div>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Branch Name</TableHead>
              <TableHead>Address</TableHead>
              <TableHead>Coordinates</TableHead>
              <TableHead>Radius</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {branches.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center h-24 text-muted-foreground">
                  {loading ? "Loading..." : "No branches configured."}
                </TableCell>
              </TableRow>
            ) : (
              branches.map((branch) => (
                <TableRow key={branch.id}>
                  <TableCell className="font-medium">{branch.name}</TableCell>
                  <TableCell className="max-w-[200px] truncate">{branch.address || "-"}</TableCell>
                  <TableCell>
                    <div className="flex items-center text-sm text-muted-foreground">
                      <Map className="h-3 w-3 mr-1" />
                      {branch.latitude?.toFixed(4)}, {branch.longitude?.toFixed(4)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">
                      {branch.radius_meters}m
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button 
                      size="sm" 
                      variant="ghost"
                      onClick={() => openDialog(branch)}
                    >
                      <Settings2 className="h-4 w-4" />
                    </Button>
                    <Button 
                      size="sm" 
                      variant="ghost"
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      onClick={() => branch.id && handleDelete(branch.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>{currentBranch ? "Edit Branch" : "Add New Branch"}</DialogTitle>
            <DialogDescription>
              Enter the branch details and geofence configuration.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right">Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="col-span-3"
                placeholder="e.g. Main Branch"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="address" className="text-right">Address</Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                className="col-span-3"
                placeholder="123 Street, City"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="lat" className="text-right">Latitude</Label>
              <Input
                id="lat"
                type="number"
                step="any"
                value={formData.latitude}
                onChange={(e) => setFormData({ ...formData, latitude: parseFloat(e.target.value) || 0 })}
                className="col-span-3"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="lon" className="text-right">Longitude</Label>
              <Input
                id="lon"
                type="number"
                step="any"
                value={formData.longitude}
                onChange={(e) => setFormData({ ...formData, longitude: parseFloat(e.target.value) || 0 })}
                className="col-span-3"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <div className="col-start-2 col-span-3">
                <Button 
                  type="button" 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                  onClick={openMapPicker}
                >
                  <MapPin className="h-4 w-4 mr-2" />
                  Pick from Map
                </Button>
              </div>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="radius" className="text-right">Radius (m)</Label>
              <Input
                id="radius"
                type="number"
                value={formData.radius_meters}
                onChange={(e) => setFormData({ ...formData, radius_meters: parseInt(e.target.value) || 0 })}
                className="col-span-3"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
              <CloseIcon className="h-4 w-4 mr-2" />
              Cancel
            </Button>
            <Button onClick={handleSave}>
              <Save className="h-4 w-4 mr-2" />
              Save Branch
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Map Picker Dialog */}
      <Dialog open={isMapOpen} onOpenChange={setIsMapOpen}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Select Location on Map</DialogTitle>
            <DialogDescription>
              Pan and zoom the map to center the crosshair over the branch location.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <MapPicker 
              initialCenter={[formData.latitude, formData.longitude]}
              onLocationSelect={(lat, lng) => setTempCoords({ lat, lng })}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsMapOpen(false)}>
              Cancel
            </Button>
            <Button onClick={confirmMapLocation}>
              Confirm Location
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      
      <p className="text-sm text-muted-foreground italic">
        * Tip: You can get coordinates from Google Maps by right-clicking a location.
      </p>
    </div>
  );
}
