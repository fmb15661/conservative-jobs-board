import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

  // 🔗 All job sources – keep this list growing but do not change UI
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
    "/jobs_alec.json",
    "/jobs_acc.json",
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
          console.error("Error loading:", src, err);
        }
      }

      setJobs(dedupeJobs(collected));
    }

    loadJobs();
  }, []);

  // Basic text normalizer
  function normalizeText(text) {
    if (!text) return "";
    return text
      .toString()
      .normalize("NFKD")
      .replace(/[\u2018\u2019]/g, "'")
      .replace(/[\u201C\u201D]/g, '"')
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  // Normalize each job shape into the format the table expects
  function normalizeJob(job) {
    if (!job || typeof job !== "object") return null;

    const rawTitle = (job.title || "").toString().trim();
    const rawOrg = (job.organization || job.org || "").toString().trim();
    const rawLocation = (job.location || job.city || "").toString().trim();
    const rawType = (job.type || "").toString().trim();
    const rawUrl = (job.url || job.link || "").toString().trim();
    const rawDate = (job.date_posted || job.date || "").toString().trim();

    if (!rawTitle || !rawUrl) return null;

    // Title case for things like ACTON all-caps
    const normalizedTitle = rawTitle
      .toLowerCase()
      .split(/\s+/)
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(" ");

    const organization = rawOrg || "N/A";
    const location = rawLocation || "N/A";
    const type = rawType || "N/A";

    return {
      title: normalizedTitle,
      organization,
      location,
      type,
      url: rawUrl,
      date: rawDate || "N/A",
    };
  }

  // ✅ DEDUPE FIX: prefer URL as the unique key
  function dedupeJobs(list) {
    const seen = new Map();

    for (const job of list) {
      if (!job) continue;

      let key;
      if (job.url) {
        // If a URL exists, that is the unique identity of the job.
        key = normalizeText(job.url);
      } else {
        // Fallback: older feeds, or weird data without URL
        key =
          normalizeText(job.title) +
          "|" +
          normalizeText(job.organization) +
          "|" +
          normalizeText(job.location);
      }

      if (!seen.has(key)) {
        seen.set(key, job);
      }
    }

    return Array.from(seen.values());
  }

  function handleSort(column) {
    if (column === sortColumn) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  }

  function getSortedJobs() {
    const sorted = [...jobs];
    sorted.sort((a, b) => {
      const aVal = (a[sortColumn] || "").toString().toLowerCase();
      const bVal = (b[sortColumn] || "").toString().toLowerCase();

      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
    return sorted;
  }

  const sortedJobs = getSortedJobs();

  const sortIndicator = (column) => {
    if (column !== sortColumn) return "";
    return sortDirection === "asc" ? " ▲" : " ▼";
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-7xl mx-auto bg-white shadow-md rounded-lg p-4">
        <h1 className="text-2xl font-bold mb-4">
          Conservative Jobs Board
        </h1>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-200">
                <th
                  className="px-3 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("title")}
                >
                  Job Title{sortIndicator("title")}
                </th>
                <th
                  className="px-3 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("organization")}
                >
                  Organization{sortIndicator("organization")}
                </th>
                <th
                  className="px-3 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("location")}
                >
                  Location{sortIndicator("location")}
                </th>
                <th
                  className="px-3 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("type")}
                >
                  Type{sortIndicator("type")}
                </th>
                <th
                  className="px-3 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("date")}
                >
                  Date Posted{sortIndicator("date")}
                </th>
              </tr>
            </thead>
            <tbody>
              {sortedJobs.map((job, idx) => (
                <tr
                  key={`${job.url}-${idx}`}
                  className={idx % 2 === 0 ? "bg-white" : "bg-gray-50"}
                >
                  <td className="border-t px-3 py-2">
                    <a
                      href={job.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {job.title}
                    </a>
                  </td>
                  <td className="border-t px-3 py-2">{job.organization}</td>
                  <td className="border-t px-3 py-2">{job.location}</td>
                  <td className="border-t px-3 py-2">{job.type}</td>
                  <td className="border-t px-3 py-2">{job.date}</td>
                </tr>
              ))}
              {sortedJobs.length === 0 && (
                <tr>
                  <td
                    colSpan="5"
                    className="text-center px-3 py-4 text-gray-500"
                  >
                    No jobs found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;

