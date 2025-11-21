import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

  // IMPORTANT: /jobs.json REMOVED
  // This ensures only *current* scraped jobs show.
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
    "/jobs_leadership_institute.json"
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
    const organization = (job.organization || "N/A").toString().trim();
    const location = (job.location || "N/A").toString().trim();
    const type = (job.type || "N/A").toString().trim();
    const url = job.url || job.link || "";

    return { title, organization, location, type, url };
  }

  function dedupeJobs(jobs) {
    const map = new Map();
    for (const job of jobs) {
      const key = normalizeText(job.url);
      if (key && !map.has(key)) {
        map.set(key, job);
      }
    }
    return Array.from(map.values());
  }

  function sortJobs(list) {
    return [...list].sort((a, b) => {
      const aVal = a[sortColumn]?.toString().toLowerCase() || "";
      const bVal = b[sortColumn]?.toString().toLowerCase() || "";

      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }

  const sortedJobs = sortJobs(jobs);

  function toggleSort(column) {
    if (column === sortColumn) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Conservative Jobs Board</h1>

      <table className="min-w-full border">
        <thead>
          <tr>
            {["title", "organization", "location", "type"].map((col) => (
              <th
                key={col}
                onClick={() => toggleSort(col)}
                className="border px-4 py-2 cursor-pointer"
              >
                {col.toUpperCase()}
                {sortColumn === col ? (sortDirection === "asc" ? " ▲" : " ▼") : ""}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedJobs.map((job, idx) => (
            <tr key={idx} className="border hover:bg-gray-100">
              <td className="border px-4 py-2">
                <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
                  {job.title}
                </a>
              </td>
              <td className="border px-4 py-2">{job.organization}</td>
              <td className="border px-4 py-2">{job.location}</td>
              <td className="border px-4 py-2">{job.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

