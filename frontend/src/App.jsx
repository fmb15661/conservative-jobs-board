import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");

  useEffect(() => {
    async function loadJobs() {
      const files = [
        "/jobs.json",
        "/jobs_talentmarket.json",
        "/jobs_yaf.json",
        "/jobs_afpi.json",
        "/jobs_cei.json",
        "/jobs_claremont.json",
        "/jobs_leadership_institute.json",
        "/jobs_tppf.json"
      ];

      let allJobs = [];

      for (const file of files) {
        try {
          const res = await fetch(file);
          if (!res.ok) continue;
          const data = await res.json();
          allJobs = allJobs.concat(data);
        } catch (err) {
          console.error("Error loading", file, err);
        }
      }

      setJobs(allJobs);
    }

    loadJobs();
  }, []);

  // SEARCH
  const filteredJobs = jobs.filter((job) => {
    const text = `${job.title} ${job.organization} ${job.location} ${job.type}`.toLowerCase();
    return text.includes(search.toLowerCase());
  });

  // SORTING
  const sortJobs = (field) => {
    let newDirection = sortDirection;

    if (sortField === field) {
      newDirection = sortDirection === "asc" ? "desc" : "asc";
      setSortDirection(newDirection);
    } else {
      setSortField(field);
      newDirection = "asc";
      setSortDirection("asc");
    }

    const sorted = [...filteredJobs].sort((a, b) => {
      const aVal = (a[field] || "").toString().toLowerCase();
      const bVal = (b[field] || "").toString().toLowerCase();

      if (aVal < bVal) return newDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return newDirection === "asc" ? 1 : -1;
      return 0;
    });

    setJobs(sorted);
  };

  const arrow = (field) => {
    if (sortField !== field) return "";
    return sortDirection === "asc" ? " ↑" : " ↓";
  };

  const displayedJobs = sortField ? jobs : filteredJobs;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Conservative Jobs Board</h1>

      <input
        type="text"
        placeholder="Search jobs..."
        className="border p-2 mb-4 w-full rounded"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse">
          <thead>
            <tr>
              <th
                className="border-b px-4 py-2 text-left cursor-pointer"
                onClick={() => sortJobs("title")}
              >
                Title {arrow("title")}
              </th>

              <th
                className="border-b px-4 py-2 text-left cursor-pointer"
                onClick={() => sortJobs("organization")}
              >
                Organization {arrow("organization")}
              </th>

              <th
                className="border-b px-4 py-2 text-left cursor-pointer"
                onClick={() => sortJobs("location")}
              >
                Location {arrow("location")}
              </th>

              <th
                className="border-b px-4 py-2 text-left cursor-pointer"
                onClick={() => sortJobs("type")}
              >
                Type {arrow("type")}
              </th>
            </tr>
          </thead>

          <tbody>
            {displayedJobs.map((job, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="border-b px-4 py-2">
                  <a
                    href={job.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-700 underline font-semibold"
                  >
                    {job.title}
                  </a>
                </td>

                <td className="border-b px-4 py-2">
                  {job.organization || "N/A"}
                </td>

                <td className="border-b px-4 py-2">
                  {job.location || "N/A"}
                </td>

                <td className="border-b px-4 py-2">
                  {job.type || "N/A"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;

