import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");

  // ALL job JSON sources, including Acton
  const sources = [
    "/jobs.json",
    "/jobs_tm.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json",
    "/jobs_ntu.json",
    "/jobs_acton.json"
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
      <h1 className="text-3xl font-bold mb-4 text-center">
        Conservative Jobs Board
      </h1>

      <table className="min-w-full bg-white border border-gray-300">
        <thead>
          <tr>
            <th
              className="py-2 px-4 border-b cursor-pointer"
              onClick={() => sortTable("title")}
            >
              Job Title
            </th>
            <th
              className="py-2 px-4 border-b cursor-pointer"
              onClick={() => sortTable("organization")}
            >
              Organization
            </th>
            <th
              className="py-2 px-4 border-b cursor-pointer"
              onClick={() => sortTable("location")}
            >
              Location
            </th>
            <th
              className="py-2 px-4 border-b cursor-pointer"
              onClick={() => sortTable("type")}
            >
              Type
            </th>
            <th className="py-2 px-4 border-b">Link</th>
          </tr>
        </thead>

        <tbody>
          {jobs.map((job, index) => (
            <tr key={index} className="hover:bg-gray-100">
              <td className="py-2 px-4 border-b">{job.title}</td>
              <td className="py-2 px-4 border-b">{job.organization}</td>
              <td className="py-2 px-4 border-b">{job.location}</td>
              <td className="py-2 px-4 border-b">{job.type}</td>
              <td className="py-2 px-4 border-b">
                <a
                  href={job.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 underline"
                >
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

