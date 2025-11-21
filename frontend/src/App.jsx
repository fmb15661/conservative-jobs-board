import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

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
    "/jobs_alec.json",
    "/jobs_crc.json",
    "/jobs_acc.json"
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

    // FIX: allow "company" as fallback for "organization"
    const organization =
      job.organization?.toString().trim() ||
      job.company?.toString().trim() ||
      "N/A";

    const location =
      (job.location || job.city || "").toString().trim() || "N/A";

    const url =
      (job.url || job.link || "").toString().trim();

    const type =
      (job.type || job.job_type || "").toString().trim() || "N/A";

    return { title, organization, location, url, type };
  }

  function dedupeJobs(jobs) {
    const seen = new Set();
    const clean = [];

    for (const job of jobs) {
      const key = normalizeText(job.url);

      if (!seen.has(key)) {
        seen.add(key);
        clean.push(job);
      }
    }
    return clean;
  }

  function sortJobs(jobs) {
    return [...jobs].sort((a, b) => {
      const aVal = (a[sortColumn] || "").toString().toLowerCase();
      const bVal = (b[sortColumn] || "").toString().toLowerCase();

      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }

  function handleSort(column) {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  }

  const sortedJobs = sortJobs(jobs);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Conservative Jobs Board</h1>

      <table className="min-w-full border-collapse border border-gray-400">
        <thead>
          <tr className="bg-gray-200">
            {["title", "organization", "location", "type"].map((col) => (
              <th
                key={col}
                className="border border-gray-400 px-2 py-1 cursor-pointer"
                onClick={() => handleSort(col)}
              >
                {col.charAt(0).toUpperCase() + col.slice(1)}
                {sortColumn === col ? (sortDirection === "asc" ? " ▲" : " ▼") : ""}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {sortedJobs.map((job, index) => (
            <tr key={index} className="hover:bg-gray-100">
              <td className="border border-gray-400 px-2 py-1">
                <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
                  {job.title}
                </a>
              </td>
              <td className="border border-gray-400 px-2 py-1">{job.organization}</td>
              <td className="border border-gray-400 px-2 py-1">{job.location}</td>
              <td className="border border-gray-400 px-2 py-1">{job.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

