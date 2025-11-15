/* eslint-disable */
import React, { useEffect, useState } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  // Load latest job data (cache-busted)
  useEffect(() => {
    const sources = [
      `/jobs.json?v=${Date.now()}`,
      `/jobs_talentmarket.json?v=${Date.now()}`,
      `/jobs_yaf.json?v=${Date.now()}`
    ];

    Promise.all(
      sources.map(src =>
        fetch(src)
          .then(res => (res.ok ? res.json() : []))
          .catch(() => [])
      )
    ).then(data => {
      const merged = data.flat();
      // remove duplicates by link
      const unique = Array.from(new Map(merged.map(j => [j.link, j])).values());
      setJobs(unique);
    });
  }, []);

  const handleSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") direction = "desc";
    setSortConfig({ key, direction });
  };

  const sortedJobs = React.useMemo(() => {
    let sortable = [...jobs];
    if (sortConfig.key) {
      sortable.sort((a, b) => {
        const valA = a[sortConfig.key]?.toString().toLowerCase() || "";
        const valB = b[sortConfig.key]?.toString().toLowerCase() || "";
        return sortConfig.direction === "asc"
          ? valA.localeCompare(valB)
          : valB.localeCompare(valA);
      });
    }
    return sortable;
  }, [jobs, sortConfig]);

  const filteredJobs = sortedJobs.filter(j =>
    [j.title, j.organization, j.location, j.type]
      .join(" ")
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center">Conservative Jobs Board</h1>

      <input
        type="text"
        placeholder="Search jobs..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="border p-2 mb-4 w-full rounded"
      />

      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300 rounded">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 cursor-pointer" onClick={() => handleSort("title")}>Title</th>
              <th className="p-2 cursor-pointer" onClick={() => handleSort("organization")}>Organization</th>
              <th className="p-2 cursor-pointer" onClick={() => handleSort("location")}>Location</th>
              <th className="p-2 cursor-pointer" onClick={() => handleSort("type")}>Type</th>
            </tr>
          </thead>
          <tbody>
            {filteredJobs.map((job, i) => (
              <tr key={i} className="border-t hover:bg-gray-50">
                <td className="p-2 text-blue-600 underline">
                  <a href={job.link} target="_blank" rel="noopener noreferrer">
                    {job.title || "N/A"}
                  </a>
                </td>
                <td className="p-2">{job.organization || "N/A"}</td>
                <td className="p-2">{job.location || "N/A"}</td>
                <td className="p-2">{job.type && job.type !== "" ? job.type : "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

