import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("All");
  const [filterLocation, setFilterLocation] = useState("All");

  useEffect(() => {
    async function fetchJobs() {
      try {
        const [res1, res2] = await Promise.all([
          fetch("/jobs.json"),
          fetch("/jobs_talentmarket.json")
        ]);
        const [jobs1, jobs2] = await Promise.all([res1.json(), res2.json()]);
        const allJobs = [...jobs1, ...jobs2];

        // Sort newest first
        allJobs.sort((a, b) => new Date(b.date_posted) - new Date(a.date_posted));

        setJobs(allJobs);
      } catch (err) {
        console.error("Error loading jobs:", err);
      }
    }

    fetchJobs();
  }, []);

  const filteredJobs = jobs.filter((job) => {
    const s = search.toLowerCase();
    return (
      (job.title?.toLowerCase().includes(s) ||
        job.organization?.toLowerCase().includes(s)) &&
      (filterType === "All" ||
        job.type?.toLowerCase() === filterType.toLowerCase()) &&
      (filterLocation === "All" ||
        job.location?.toLowerCase().includes(filterLocation.toLowerCase()))
    );
  });

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Conservative Jobs Board</h1>

      {/* Search & Filters */}
      <div className="flex flex-col md:flex-row md:items-center md:space-x-4 mb-6">
        <input
          type="text"
          placeholder="Search job titles or organizations..."
          className="flex-1 border rounded-lg p-2 mb-2 md:mb-0"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          className="border rounded-lg p-2"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
        >
          <option>All</option>
          <option>Full-time</option>
          <option>Part-time</option>
          <option>Internship</option>
          <option>Fellowship</option>
        </select>

        <input
          type="text"
          placeholder="Filter by location..."
          className="border rounded-lg p-2"
          value={filterLocation === "All" ? "" : filterLocation}
          onChange={(e) => setFilterLocation(e.target.value || "All")}
        />
      </div>

      {/* Jobs Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-4 py-2 text-left">Job Title</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Organization</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Location</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Type</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Date Posted</th>
            </tr>
          </thead>
          <tbody>
            {filteredJobs.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center p-4 text-gray-500">
                  No jobs match your filters.
                </td>
              </tr>
            ) : (
              filteredJobs.map((job, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="border border-gray-300 px-4 py-2">
                    <a
                      href={job.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {job.title}
                    </a>
                  </td>
                  <td className="border border-gray-300 px-4 py-2">{job.organization}</td>
                  <td className="border border-gray-300 px-4 py-2">{job.location}</td>
                  <td className="border border-gray-300 px-4 py-2">{job.type}</td>
                  <td className="border border-gray-300 px-4 py-2">{job.date_posted}</td>
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

