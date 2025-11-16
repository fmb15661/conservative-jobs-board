import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");

  // List of job JSON sources (PLF added at the bottom)
  const sources = [
    "/jobs.json",
    "/jobs_tm.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json"   // ⬅️ Added PLF here, last in list
  ];

  useEffect(() => {
    async function loadJobs() {
      let all = [];

      for (const src of sources) {
        try {
          const response = await fetch(src);
          if (response.ok) {
            const data = await response.json();
            all = [...all, ...data];
          }
        } catch (e) {
          console.log("Failed to load:", src);
        }
      }

      setJobs(all);
    }

    loadJobs();
  }, []);

  const sortTable = (column) => {
    let direction = sortDirection;

    if (sortColumn === column) {
      direction = direction === "asc" ? "desc" : "asc";
    } else {
      direction = "asc";
    }

    const sorted = [...jobs].sort((a, b) => {
      const x = a[column] ? a[column].toString().toLowerCase() : "";
      const y = b[column] ? b[column].toString().toLowerCase() : "";

      if (x < y) return direction === "asc" ? -1 : 1;
      if (x > y) return direction === "asc" ? 1 : -1;
      return 0;
    });

    setSortColumn(column);
    setSortDirection(direction);
    setJobs(sorted);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Conservative Jobs Board
      </h1>

      <table className="min-w-full border border-gray-400">
        <thead>
          <tr className="bg-gray-200">
            <th
              className="p-2 border cursor-pointer"
              onClick={() => sortTable("title")}
            >
              Job Title
            </th>
            <th
              className="p-2 border cursor-pointer"
              onClick={() => sortTable("organization")}
            >
              Organization
            </th>
            <th
              className="p-2 border cursor-pointer"
              onClick={() => sortTable("location")}
            >
              Location
            </th>
            <th
              className="p-2 border cursor-pointer"
              onClick={() => sortTable("type")}
            >
              Type
            </th>
            <th
              className="p-2 border cursor-pointer"
              onClick={() => sortTable("date_posted")}
            >
              Date Posted
            </th>
            <th className="p-2 border">Link</th>
          </tr>
        </thead>

        <tbody>
          {jobs.map((job, index) => (
            <tr key={index} className="border">
              <td className="p-2 border">{job.title}</td>
              <td className="p-2 border">{job.organization}</td>
              <td className="p-2 border">{job.location}</td>
              <td className="p-2 border">{job.type}</td>
              <td className="p-2 border">{job.date_posted}</td>
              <td className="p-2 border text-blue-600 underline">
                <a href={job.link} target="_blank" rel="noopener noreferrer">
                  Apply
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

