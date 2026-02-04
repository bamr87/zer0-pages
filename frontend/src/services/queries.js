import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from './api'

// Auth
export const useLogin = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (credentials) => {
      const response = await api.post('/api/auth/token/', credentials)
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user'])
    },
  })
}

// Posts
export const usePosts = () => {
  return useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const response = await api.get('/api/content/posts/')
      return response.data
    },
  })
}

export const useCreatePost = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (postData) => {
      const response = await api.post('/api/content/posts/', postData)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['posts'])
    },
  })
}

// Pages
export const usePages = () => {
  return useQuery({
    queryKey: ['pages'],
    queryFn: async () => {
      const response = await api.get('/api/content/pages/')
      return response.data
    },
  })
}

// PRDs
export const usePRDs = () => {
  return useQuery({
    queryKey: ['prds'],
    queryFn: async () => {
      const response = await api.get('/api/prd/prds/')
      return response.data
    },
  })
}

// Settings
export const useSettings = () => {
  return useQuery({
    queryKey: ['settings'],
    queryFn: async () => {
      const response = await api.get('/api/settings/')
      return response.data
    },
  })
}

export const useUpdateSettings = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (settings) => {
      const response = await api.post('/api/settings/', settings)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['settings'])
    },
  })
}



