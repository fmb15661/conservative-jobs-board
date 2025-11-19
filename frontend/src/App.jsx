import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

  const sources = [
    "/jobs.json",
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
    "/jobs_crc.json"     // <-- ADDED CRC SOURCE
  ];

  useEffect(() => {
    async function loadJobs() {
      const collected = [];

      for (const src of sources) {
        try {
          const res = await fetch(src);
          if (!res.ok) continue;

          const data = await res.json();
          if (!Array.isArray(data)) continue;

          data.forEach((raw) => {
            const normalized = normalizeJob(raw);
            if (normalized && normalized.title && normalized.url) {
              collected.push(normalized);
            }
          });
        } catch (err) {
          console.error("Error loading: ", src, err);
        }
      }

      setJobs(dedupeJobs(collected));
    }

    loadJobs();
  }, []);

  function normalizeText(text) {
    if (!text) return "";
    return text
      .normalize("NFKD")
      .replace(/[\u2018\u2019\u201C\u201D]/g, "'")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function normalizeJob(job) {
    const title = (job.title || "").toString().trim();

    // Accept both "url" and "link"
    const url = (job.url || job.link || "").toString().trim();

    const organization =
      job.organization || job.company || "N/A";

    const location = job.location || "N/A";
    const type = job.type || "N/A";

    return {
      title,
      organization,
      location,
      url,
      type
    };
  }

  function dedupeJobs(list) {
    const seen = new Set();
    const result = [];

    for (const job of list) {
      const key = normalizeText(job.title) + "|" + normalizeText(job.organization);
      if (!seen.has(key)) {
        seen.add(key);
        result.push(job);
      }
    }
    return result;
  }

  function sortJobs(jobs, column, direction) {
    return [...jobs].sort((a, b) => {
      const valA = (a[column] || "").toString().toLowerCase();
      const valB = (b[column] || "").toString().toLowerCase();

      if (valA < valB) return direction === "asc" ? -1 : 1;
      if (valA > valB) return direction === "asc" ? 1 : -1;
      return 0;
    });
  }

  const sortedJobs = sortJobs(jobs, sortColumn, sortDirection);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Conservative Jobs Board</h1>
      <table className="min-w-full border-collapse border border-gray-400">
        <thead>
          <tr>
            {["title", "organization", "location", "type"].map((col) => (
              <th
                key={col}
                onClick={() => {
                  if (sortColumn === col) {
                    setSortDirection(sortDirection === "asc" ? "desc" : "asc");
                  } else {
                    setSortColumn(col);
                    setSortDirection("asc");
                  }
                }}
                className="border border-gray-400 p-2 cursor-pointer bg-gray-100"
              >
                {col[0].toUpperCase() + col.slice(1)}
                {sortColumn === col ? (sortDirection === "asc" ? " ▲" : " ▼") : ""}
              </th>
            ))}
            <th className="border border-gray-400 p-2 bg-gray-100">Apply</th>
          </tr>
        </thead>
        <tbody>
          {sortedJobs.map((job, idx) => (
            <tr key={idx} className="hover:bg-gray-50">
              <td className="border border-gray-400 p-2">{job.title}</td>
              <td className="border border-gray-400 p-2">{job.organization}</td>
              <td className="border border-gray-400 p-2">{job.location}</td>
              <td className="border border-gray-400 p-2">{job.type}</td>
              <td className="border border-gray-400 p-2">
                <a
                  href={job.url}
                  className="text-blue-600 underline"
                  target="_blank"
                  rel="noopener noreferrer"
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

