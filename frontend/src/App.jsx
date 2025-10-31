import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadJobs() {
      try {
        const files = ["/jobs.json", "/jobs_talentmarket.json"];
        const allData = [];

        for (const file of files) {
          const res = await fetch(file);
          const data = await res.json();
          if (Array.isArray(data)) allData.push(...data);
        }

        // Sort newest first
        allData.sort((a, b) => new Date(b.date_posted) - new Date(a.date_posted));
        setJobs(allData);
      } catch (err) {
        console.error("❌ Error loading job data:", err);
      }
    }
    loadJobs();
  }, []);

  const filtered = jobs.filter((job) => {
    const q = search.toLowerCase();
    return (
      job.title?.toLowerCase().includes(q) ||
      job.organization?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Conservative Jobs Board
      </h1>

      <input
        type="text"
        placeholder="Search jobs..."
        className="w-full border p-2 rounded mb-4"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-4 py-2 text-left">Job Title</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Organization</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Location</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Date Posted</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan="4" className="text-center p-4 text-gray-500">
                  No jobs found
                </td>
              </tr>
            ) : (
              filtered.map((job, i) => (
                <tr key={i} className="hover:bg-gray-50">
                  <td className="border border-gray-300 px-4 py-2">
                    <a href={job.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                      {job.title}
                    </a>
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {job.organization || "N/A"}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {job.location || "N/A"}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {job.date_posted || "N/A"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;

