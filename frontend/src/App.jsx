import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  const sources = [
    "/jobs_talentmarket.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json",
    "/jobs_ntu.json",
    "/jobs_acton.json",
    "/jobs_aier.json",
    "/jobs_excelined.json",
    "/jobs_claremont.json",
    "/jobs_heritage.json",
    "/jobs_cei.json",
    "/jobs_tppf.json",
    "/jobs_leadership_institute.json",
    "/jobs_crc.json",
    "/jobs_alec.json",
    "/jobs_acc.json",
    "/jobs_amprinproj.json",
    "/jobs_ashbrook.json",
    "/jobs_bri.json",
    "/jobs_commonwealth.json" 
  ];

  useEffect(() => {
    async function loadJobs() {
      let allJobs = [];

      for (const src of sources) {
        try {
          const res = await fetch(src);
          const data = await res.json();

          const normalized = data.map((job) => ({
            title: job.title || "N/A",
            organization: job.organization || job.org || "N/A",
            location: job.location || "N/A",
            url: job.url || job.link || "#"
          }));

          allJobs = [...allJobs, ...normalized];
        } catch (err) {
          console.error("Error loading", src, err);
        }
      }

      setJobs(allJobs);
    }

    loadJobs();
  }, []);

  const sortBy = (key) => {
    let direction = "asc";

    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }

    setSortConfig({ key, direction });

    const sorted = [...jobs].sort((a, b) => {
      if (!a[key]) return 1;
      if (!b[key]) return -1;

      const aVal = a[key].toUpperCase();
      const bVal = b[key].toUpperCase();

      if (aVal < bVal) return direction === "asc" ? -1 : 1;
      if (aVal > bVal) return direction === "asc" ? 1 : -1;
      return 0;
    });

    setJobs(sorted);
  };

  return (
    <div className="container mx-auto px-6 py-6">
      <h1 className="text-3xl font-bold mb-6">Conservative Jobs Board</h1>

      <table className="min-w-full border border-gray-300">
        <thead>
          <tr>
            <th className="border px-4 py-2 cursor-pointer" onClick={() => sortBy("title")}>
              Job Title
            </th>
            <th className="border px-4 py-2 cursor-pointer" onClick={() => sortBy("organization")}>
              Organization
            </th>
            <th className="border px-4 py-2 cursor-pointer" onClick={() => sortBy("location")}>
              Location
            </th>
            <th className="border px-4 py-2">Link</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job, idx) => (
            <tr key={idx} className="hover:bg-gray-100">
              <td className="border px-4 py-2">{job.title}</td>
              <td className="border px-4 py-2">{job.organization}</td>
              <td className="border px-4 py-2">{job.location}</td>
              <td className="border px-4 py-2">
                <a
                  href={job.url}
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

