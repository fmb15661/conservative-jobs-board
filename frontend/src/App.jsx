import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

  // === ALL WORKING SOURCES ===
  const sources = [
    "/jobs_acc.json",
    "/jobs_acton.json",
    "/jobs_afpi.json",
    "/jobs_aier.json",
    "/jobs_alec.json",
    "/jobs_cato.json",
    "/jobs_cei.json",
    "/jobs_claremont.json",
    "/jobs_crc.json",
    "/jobs_excelined.json",
    "/jobs_heritage.json",
    "/jobs_hudson.json",
    "/jobs_leadership_institute.json",
    "/jobs_ntu.json",
    "/jobs_plf.json",
    "/jobs_talentmarket.json",
    "/jobs_tppf.json",
    "/jobs_yaf.json"
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

          data.forEach(raw => {
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

  // === NORMALIZATION ===
  function normalizeJob(job) {
    const title = (job.title || "").toString().trim();
    const organization = (job.organization || "").toString().trim();
    const location = (job.location || "").toString().trim();
    const type = (job.type || "").toString().trim() || "N/A";

    // accept "url" or "link"
    const url = job.url || job.link || "";

    if (!title || !url) return null;

    return {
      title,
      organization,
      location,
      type,
      url
    };
  }

  // === DEDUPE: FIXES TM DUPLICATES ===
  function dedupeJobs(list) {
    const map = new Map();
    for (const job of list) {
      const key = normalizeText(job.url);
      if (!map.has(key)) {
        map.set(key, job);
      }
    }
    return Array.from(map.values());
  }

  // === SORTING ===
  function sortBy(column) {
    const direction =
      sortColumn === column && sortDirection === "asc" ? "desc" : "asc";

    const sorted = [...jobs].sort((a, b) => {
      const aVal = (a[column] || "").toLowerCase();
      const bVal = (b[column] || "").toLowerCase();

      if (aVal < bVal) return direction === "asc" ? -1 : 1;
      if (aVal > bVal) return direction === "asc" ? 1 : -1;
      return 0;
    });

    setSortColumn(column);
    setSortDirection(direction);
    setJobs(sorted);
  }

  return (
    <div className="container mx-auto p-4">
      <table className="min-w-full table-auto border-collapse border border-gray-400">
        <thead>
          <tr>
            <th onClick={() => sortBy("title")} className="border px-4 py-2 cursor-pointer">Job Title</th>
            <th onClick={() => sortBy("organization")} className="border px-4 py-2 cursor-pointer">Organization</th>
            <th onClick={() => sortBy("location")} className="border px-4 py-2 cursor-pointer">Location</th>
            <th onClick={() => sortBy("type")} className="border px-4 py-2 cursor-pointer">Type</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job, idx) => (
            <tr key={idx} className="hover:bg-gray-200">
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

