import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  useEffect(() => {
    async function loadJobs() {
      const files = [
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

  function sortBy(field) {
    const newOrder = sortField === field && sortOrder === "asc" ? "desc" : "asc";
    setSortField(field);
    setSortOrder(newOrder);

    const sorted = [...jobs].sort((a, b) => {
      const x = (a[field] || "").toString().toLowerCase();
      const y = (b[field] || "").toString().toLowerCase();

      if (x < y) return newOrder === "asc" ? -1 : 1;
      if (x > y) return newOrder === "asc" ? 1 : -1;
      return 0;
    });

    setJobs(sorted);
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Conservative Jobs Board</h1>

      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-2 cursor-pointer" onClick={() => sortBy("title")}>
              Job Title
            </th>
            <th className="p-2 cursor-pointer" onClick={() => sortBy("organization")}>
              Organization
            </th>
            <th className="p-2 cursor-pointer" onClick={() => sortBy("location")}>
              Location
            </th>
            <th className="p-2 cursor-pointer" onClick={() => sortBy("type")}>
              Type
            </th>
          </tr>
        </thead>

        <tbody>
          {jobs.map((job, index) => (
            <tr key={index} className="border-b hover:bg-gray-100">
              <td className="p-2">
                <a
                  href={job.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-700 underline"
                >
                  {job.title}
                </a>
              </td>

              <td className="p-2">{job.organization}</td>
              <td className="p-2">{job.location || "N/A"}</td>
              <td className="p-2">{job.type || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

