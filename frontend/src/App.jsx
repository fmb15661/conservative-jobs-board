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
    "/jobs_crc.json",
    "/jobs_alec.json"
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

    // 🔥 FIXED: supports every possible org key
    const organization =
      job.organization ||
      job.org ||
      job.company ||
      job.company_name ||
      job.employer ||
      "N/A";

    const location = (job.location || "").toString().trim();
    const url =
      job.link || job.url || job.apply_link || job.apply_url || "";

    return {
      title,
      organization: organization.toString().trim(),
      location: detectVirtual(location),
      url,
      type: job.type || "N/A"
    };
  }

  function detectVirtual(location) {
    if (!location) return "N/A";
    const loc = location.toLowerCase();
    if (loc.includes("virtual") || loc.includes("remote")) {
      return "Virtual";
    }
    return location;
  }

  function dedupeJobs(list) {
    const seen = new Set();
    const output = [];

    list.forEach((job) => {
      const key = normalizeText(job.title) + "|" + normalizeText(job.organization);
      if (!seen.has(key)) {
        seen.add(key);
        output.push(job);
      }
    });

    return output;
  }

  function sortJobs(jobs) {
    return [...jobs].sort((a, b) => {
      const valA = normalizeText(a[sortColumn]);
      const valB = normalizeText(b[sortColumn]);
      if (valA < valB) return sortDirection === "asc" ? -1 : 1;
      if (valA > valB) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }

  function handleSort(column) {
    if (column === sortColumn) {
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

      <table className="table-auto w-full border-collapse border border-gray-400">
        <thead>
          <tr>
            {["title", "organization", "location", "type"].map((col) => (
              <th
                key={col}
                onClick={() => handleSort(col)}
                className="border border-gray-400 px-2 py-1 cursor-pointer bg-gray-100"
              >
                {col.charAt(0).toUpperCase() + col.slice(1)}
                {sortColumn === col ? (sortDirection === "asc" ? " ▲" : " ▼") : ""}
              </th>
            ))}
            <th className="border border-gray-400 px-2 py-1 bg-gray-100">Link</th>
          </tr>
        </thead>

        <tbody>
          {sortedJobs.map((job, idx) => (
            <tr key={idx} className="border border-gray-300">
              <td className="border px-2 py-1">{job.title}</td>
              <td className="border px-2 py-1">{job.organization}</td>
              <td className="border px-2 py-1">{job.location}</td>
              <td className="border px-2 py-1">{job.type}</td>
              <td className="border px-2 py-1">
                <a href={job.url} className="text-blue-600 underline" target="_blank" rel="noreferrer">
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

