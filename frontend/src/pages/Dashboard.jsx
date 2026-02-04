import { usePosts, usePRDs } from '../services/queries'

export default function Dashboard() {
  const { data: posts, isLoading: postsLoading } = usePosts()
  const { data: prds, isLoading: prdsLoading } = usePRDs()

  const postCount = posts?.results?.length || posts?.length || 0
  const prdCount = prds?.results?.length || prds?.length || 0

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-gray-500 text-sm uppercase font-semibold">Total Posts</h3>
          {postsLoading ? (
            <p className="text-3xl font-bold mt-2">...</p>
          ) : (
            <p className="text-3xl font-bold mt-2">{postCount}</p>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-gray-500 text-sm uppercase font-semibold">Active PRDs</h3>
          {prdsLoading ? (
            <p className="text-3xl font-bold mt-2">...</p>
          ) : (
            <p className="text-3xl font-bold mt-2">{prdCount}</p>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-gray-500 text-sm uppercase font-semibold">Site Visitors</h3>
          <p className="text-3xl font-bold mt-2">-</p>
        </div>
      </div>
    </div>
  )
}
