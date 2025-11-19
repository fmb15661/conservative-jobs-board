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
    "/jobs_excelined.json"
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
      .replace(/[\u2018\u2019\u201C\u201D]/g, "'") // smart quotes → normal
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function normalizeJob(job) {
    const title = (job.title || "").toString().trim();
    const organization =
      (job.organization ||
        job.company ||
        job.employer ||
        "N/A").toString().trim();

    const url = (job.url || job.link || "").toString().trim();

    let rawLocation = (job.location || "").toString().trim();
    let jobType = (job.type || "").toString().trim() || "N/A";

    const description = (job.description || "").toString().trim();

    const normDesc = normalizeText(description);
    const normLoc = normalizeText(rawLocation);

    let finalLocation = "N/A";

    if (normDesc.includes("virtual") || normDesc.includes("remote")) {
      finalLocation = "Virtual";
    } else if (normLoc.includes("virtual") || normLoc.includes("remote")) {
      finalLocation = "Virtual";
    } else if (rawLocation) {
      finalLocation = rawLocation;
    }

    return {
      title,
      organization,
      location: finalLocation,
      type: jobType,
      url
    };
  }

  function dedupeJobs(arr) {
    const seen = new Set();
    const result = [];

    for (const job of arr) {
      const key = `${job.title.toLowerCase()}||${job.organization.toLowerCase()}||${job.url}`;
      if (seen.has(key)) continue;
      seen.add(key);
      result.push(job);
    }

    return result;
  }

  function handleSort(column) {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  }

  function getSortedJobs() {
    const sortable = [...jobs];
    sortable.sort((a, b) => {
      const x = (a[sortColumn] || "").toLowerCase();
      const y = (b[sortColumn] || "").toLowerCase();
      if (x < y) return sortDirection === "asc" ? -1 : 1;
      if (x > y) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
    return sortable;
  }

  const sortedJobs = getSortedJobs();

  const arrow = (column) =>
    sortColumn === column ? (sortDirection === "asc" ? " ▲" : " ▼") : "";

  return (
    <div style={{ padding: "20px" }}>
      <h1>Conservative Jobs Board</h1>

      <table border="1" width="100%" cellPadding="8" cellSpacing="0">
        <thead>
          <tr>
            <th style={{ cursor: "pointer" }} onClick={() => handleSort("title")}>
              Title{arrow("title")}
            </th>
            <th
              style={{ cursor: "pointer" }}
              onClick={() => handleSort("organization")}
            >
              Organization{arrow("organization")}
            </th>
            <th
              style={{ cursor: "pointer" }}
              onClick={() => handleSort("location")}
            >
              Location{arrow("location")}
            </th>
            <th style={{ cursor: "pointer" }} onClick={() => handleSort("type")}>
              Type{arrow("type")}
            </th>
            <th>Link</th>
          </tr>
        </thead>

        <tbody>
          {sortedJobs.map((job, i) => (
            <tr key={i}>
              <td>{job.title}</td>
              <td>{job.organization}</td>
              <td>{job.location}</td>
              <td>{job.type}</td>
              <td>
                <a href={job.url} target="_blank">
                  Apply
                </a>
              </td>
            </tr>
          ))}

          {sortedJobs.length === 0 && (
            <tr>
              <td colSpan="5" style={{ textAlign: "center" }}>
                No jobs found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;

