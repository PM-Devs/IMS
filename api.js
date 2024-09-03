import axios from 'axios';

const API_BASE_URL = 'https://your-api-base-url.com';

// Create an axios instance with default headers
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-App-ID': 'your-app-id',
    'X-App-Key': 'your-app-key',
  },
});

// Interceptor to add Authorization header for authenticated requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const login = async (username, password, scope = 'R-WR-R-R') => {
  const response = await api.post('/login', {
    grant_type: 'password',
    username,
    password,
    scope,
  });
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/logout');
  return response.data;
};

export const getDashboard = async () => {
  const response = await api.get('/dashboard');
  return response.data;
};

export const searchStudents = async (query) => {
  const response = await api.get('/students/search', { params: { query } });
  return response.data;
};

export const getStudentList = async (status = null) => {
  const response = await api.get('/students', { params: { status } });
  return response.data;
};

export const updateStudentStatus = async (studentId, status) => {
  const response = await api.put(`/students/${studentId}/status`, { status });
  return response.data;
};

export const getStudentLocation = async (studentId) => {
  const response = await api.get(`/students/${studentId}/location`);
  return response.data;
};

export const isStudentAtCompany = async (studentId, companyId, maxDistance = 200) => {
  const response = await api.get(`/students/${studentId}/at-company/${companyId}`, {
    params: { max_distance: maxDistance },
  });
  return response.data;
};

export const getVisitLocations = async () => {
  const response = await api.get('/visit-locations');
  return response.data;
};

export const createVisitLocation = async (visitData) => {
  const response = await api.post('/visit-locations', visitData);
  return response.data;
};

export const updateVisitLocation = async (visitLocationId, visitLocation) => {
  const response = await api.put(`/visit-locations/${visitLocationId}`, visitLocation);
  return response.data;
};

export const deleteVisitLocation = async (visitLocationId) => {
  const response = await api.delete(`/visit-locations/${visitLocationId}`);
  return response.data;
};

export const updateVisitStatus = async (visitId, status) => {
  const response = await api.put(`/visit-locations/${visitId}/status`, { status });
  return response.data;
};

export const getSupervisorProfile = async () => {
  const response = await api.get('/profile');
  return response.data;
};

export const updateSupervisorProfile = async (profileData) => {
  const response = await api.put('/profile', profileData);
  return response.data;
};

export const deleteSupervisorProfile = async () => {
  const response = await api.delete('/profile');
  return response.data;
};

export const getStudentLogs = async (studentId, logType) => {
  const response = await api.get(`/logs/${studentId}/${logType}`);
  return response.data;
};

export const markLogbookEntry = async (logbookId, status, comments = null) => {
  const response = await api.put(`/logs/${logbookId}/mark`, { status, comments });
  return response.data;
};

export const createFinalReport = async (studentId, reportData) => {
  const response = await api.post('/final-reports', { student_id: studentId, ...reportData });
  return response.data;
};

export const updateFinalReport = async (reportId, reportData) => {
  const response = await api.put(`/final-reports/${reportId}`, reportData);
  return response.data;
};

export const getFinalReport = async (reportId) => {
  const response = await api.get(`/final-reports/${reportId}`);
  return response.data;
};

export const deleteFinalReport = async (reportId) => {
  const response = await api.delete(`/final-reports/${reportId}`);
  return response.data;
};

export const createEvaluation = async (studentId, evaluationData) => {
  const response = await api.post('/evaluations', { student_id: studentId, ...evaluationData });
  return response.data;
};

export const generateEvaluationReport = async (studentId) => {
  const response = await api.get(`/evaluations/${studentId}/report`);
  return response.data;
};

export const assignSupervisorToZone = async (supervisorId, zoneId) => {
  const response = await api.put(`/zones/${supervisorId}/assign`, { zone_id: zoneId });
  return response.data;
};

export const getSupervisorsInZone = async (zoneId) => {
  const response = await api.get(`/zones/${zoneId}/supervisors`);
  return response.data;
};

export const assignStudentsToSupervisor = async (supervisorId, studentIds) => {
  const response = await api.put(`/supervisors/${supervisorId}/assign-students`, { student_ids: studentIds });
  return response.data;
};

export const getAssignedStudents = async (supervisorId) => {
  const response = await api.get(`/supervisors/${supervisorId}/assigned-students`);
  return response.data;
};

export const getSupervisorWorkload = async (supervisorId) => {
  const response = await api.get(`/supervisors/${supervisorId}/workload`);
  return response.data;
};

export const balanceSupervisorWorkload = async (zoneId) => {
  const response = await api.put(`/zones/${zoneId}/balance-workload`);
  return response.data;
};

export const manageSupervisorWorkload = async () => {
  const response = await api.put('/workload/manage');
  return response.data;
};

export const getZoneChat = async (zoneId) => {
  const response = await api.get(`/zones/${zoneId}/chat`);
  return response.data;
};

export const addMessageToZoneChat = async (zoneId, content) => {
  const response = await api.post(`/zones/${zoneId}/chat/message`, { content });
  return response.data;
};

export const getZoneChatMessages = async (zoneId, limit = 50, skip = 0) => {
  const response = await api.get(`/zones/${zoneId}/chat/messages`, {
    params: { limit, skip },
  });
  return response.data;
};