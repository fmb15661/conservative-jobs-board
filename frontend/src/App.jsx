import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("All");
  const [filterLocation, setFilterLocation] = useState("All");

  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/jobs.json")
      .then((res) => res.json())
      .then((data) => {
        if (!Array.isArray(data)) {
          console.error("Invalid jobs.json format");
          return;
        }

        // Filter out any broken/null entries
        const cleanData = data.filter(
          (job) => job && typeof job === "object" && job.title
        );

        // Sort newest first
        const sorted = [...cleanData].sort((a, b) => {
          const dateA = new Date(a.date_posted || "1970-01-01");
          const dateB = new Date(b.date_posted || "1970-01-01");
          return dateB - dateA;
        });

        setJobs(sorted);
      })
      .catch((err) => console.error("Error loading jobs.json", err));
  }, []);

  const filteredJobs = jobs.filter((job) => {
    const title = (job.title || "").toLowerCase();
    const org = (job.organization || "").toLowerCase();
    const type = (job.type || "").toLowerCase();
    const location = (job.location || "").toLowerCase();

    const matchesSearch =
      title.includes(search.toLowerCase()) ||
      org.includes(search.toLowerCase());

    const matchesType =
      filterType === "All" || type === filterType.toLowerCase();

    const matchesLocation =
      filterLocation === "All" ||
      location.includes(filterLocation.toLowerCase());

    return matchesSearch && matchesType && matchesLocation;
  });

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Conservative Jobs Board
      </h1>

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
                      href={job.link || "#"}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {job.title || "View Jobs"}
                    </a>
                  </td>
                  <td className="border border-gray-300 px-4 py-2">{job.organization || "N/A"}</td>
                  <td className="border border-gray-300 px-4 py-2">{job.location || "N/A"}</td>
                  <td className="border border-gray-300 px-4 py-2">{job.type || "N/A"}</td>
                  <td className="border border-gray-300 px-4 py-2">{job.date_posted || "N/A"}</td>
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
