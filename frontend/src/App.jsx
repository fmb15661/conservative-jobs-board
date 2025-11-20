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
    "/jobs_acc.json"   // ✅ ADDED
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

    const orgFields = [
      job.organization,
      job.company,
      job.org,
      job.employer,
      job.source
    ];

    let organization = "";
    for (const f of orgFields) {
      if (f && typeof f === "string" && f.trim() !== "") {
        organization = f.trim();
        break;
      }
    }

    if (!organization) organization = "N/A";

    const location = (job.location || job.city || "").toString().trim() || "N/A";
    const url = (job.link || job.url || "").toString().trim();
    const type = (job.type || job.job_type || "").toString().trim() || "N/A";

    return {
      title,
      organization,
      location,
      url,
      type
    };
  }

  function dedupeJobs(list) {
    const seen = new Map();

    for (const job of list) {
      const key = normalizeText(job.title) + normalizeText(job.organization);
      if (!seen.has(key)) {
        seen.set(key, job);
      }
    }

    return Array.from(seen.values());
  }

  function sortJobs(list) {
    if (!sortColumn) return list;

    const sorted = [...list].sort((a, b) => {
      const aVal = (a[sortColumn] || "").toString().toLowerCase();
      const bVal = (b[sortColumn] || "").toString().toLowerCase();

      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });

    return sorted;
  }

  function handleSort(col) {
    if (sortColumn === col) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(col);
      setSortDirection("asc");
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Conservative Jobs Board</h1>

      <table className="table-auto w-full border-collapse border border-gray-400">
        <thead>
          <tr className="bg-gray-200">
            {["title", "organization", "location", "type"].map((col) => (
              <th
                key={col}
                className="border border-gray-400 p-2 cursor-pointer"
                onClick={() => handleSort(col)}
              >
                {col.toUpperCase()}{" "}
                {sortColumn === col ? (sortDirection === "asc" ? "▲" : "▼") : ""}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {sortJobs(jobs).map((job, idx) => (
            <tr key={idx} className="border border-gray-400">
              <td className="border p-2">
                <a
                  href={job.url}
                  className="text-blue-600 underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {job.title}
                </a>
              </td>
              <td className="border p-2">{job.organization}</td>
              <td className="border p-2">{job.location}</td>
              <td className="border p-2">{job.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

