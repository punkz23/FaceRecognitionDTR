import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/auth/LoginPage';
import ProtectedLayout from './layouts/ProtectedLayout';
import ApprovalQueue from './pages/admin/ApprovalQueue';
import EmployeeManagement from './pages/admin/EmployeeManagement';
import DTRDashboard from './pages/admin/DTRDashboard';
import BranchManagement from './pages/admin/BranchManagement';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

function Dashboard() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
      
      <Tabs defaultValue="approvals" className="w-full">
        <TabsList className="mb-4">
          <TabsTrigger value="approvals">Pending Approvals</TabsTrigger>
          <TabsTrigger value="employees">Employee Management</TabsTrigger>
          <TabsTrigger value="dtr">DTR Monitoring</TabsTrigger>
          <TabsTrigger value="branches">Branch Settings</TabsTrigger>
        </TabsList>
        <TabsContent value="approvals">
          <ApprovalQueue />
        </TabsContent>
        <TabsContent value="employees">
          <EmployeeManagement />
        </TabsContent>
        <TabsContent value="dtr">
          <DTRDashboard />
        </TabsContent>
        <TabsContent value="branches">
          <BranchManagement />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
