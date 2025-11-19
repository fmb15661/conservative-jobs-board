import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

  // All JSON feeds, including ExcelinEd
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
    "/jobs_excelined.json",
  ];

  useEffect(() => {
    async function loadJobs() {
      const allJobs = [];

      for (const src of sources) {
        try {
          const res = await fetch(src);
          if (!res.ok) continue;

          const data = await res.json();
          if (!Array.isArray(data)) continue;

          data.forEach((raw) => {
            const normalized = normalizeJob(raw);
            if (normalized && normalized.title && normalized.url) {
              allJobs.push(normalized);
            }
          });
        } catch (err) {
          console.error("Error loading jobs from", src, err);
        }
      }

      const deduped = dedupeJobs(allJobs);
      setJobs(deduped);
    }

    loadJobs();
  }, []);

  function normalizeJob(job) {
    // Title
    const title =
      (job.title ||
        job.position ||
        job.job_title ||
        "").toString().trim();

    // Organization / company
    const organization =
      (job.organization ||
        job.company ||
        job.employer ||
        "").toString().trim();

    // URL
    const url =
      (job.link ||
        job.url ||
        job.apply_url ||
        "").toString().trim();

    // Raw location and type
    const rawLocation =
      (job.location ||
        job.city ||
        job.region ||
        "").toString().trim();

    const rawType =
      (job.type ||
        job.job_type ||
        "").toString().trim();

    // Description (for virtual detection)
    const description =
      (job.description ||
        job.desc ||
        job.summary ||
        "").toString().trim();

    const descLower = description.toLowerCase();
    let location = rawLocation;

    // If the location string itself says anything about virtual, simplify it
    if (location) {
      if (location.toLowerCase().includes("virtual")) {
        location = "Virtual";
      }
    } else {
      // No explicit location – infer from description if possible
      if (descLower.includes("virtual")) {
        location = "Virtual";
      } else {
        location = "N/A";
      }
    }

    // Normalize type – we are not really using it yet, so default to N/A if blank
    const type = rawType || "N/A";

    return {
      title,
      organization: organization || "N/A",
      location,
      type,
      url,
    };
  }

  function dedupeJobs(list) {
    const seen = new Set();
    const result = [];

    for (const job of list) {
      const key = `${job.title.toLowerCase()}||${job.organization.toLowerCase()}||${job.url}`;
      if (seen.has(key)) continue;
      seen.add(key);
      result.push(job);
    }

    return result;
  }

  function handleSort(column) {
    if (sortColumn === column) {
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

  const renderSortArrow = (column) => {
    if (sortColumn !== column) return "";
    return sortDirection === "asc" ? " ▲" : " ▼";
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">
        Conservative Jobs Board
      </h1>

      <div className="overflow-x-auto bg-white shadow rounded-lg">
        <table className="min-w-full border-collapse">
          <thead>
            <tr className="bg-gray-200">
              <th
                className="px-4 py-2 border cursor-pointer text-left"
                onClick={() => handleSort("title")}
              >
                Job Title{renderSortArrow("title")}
              </th>
              <th
                className="px-4 py-2 border cursor-pointer text-left"
                onClick={() => handleSort("organization")}
              >
                Organization{renderSortArrow("organization")}
              </th>
              <th
                className="px-4 py-2 border cursor-pointer text-left"
                onClick={() => handleSort("location")}
              >
                Location{renderSortArrow("location")}
              </th>
              <th
                className="px-4 py-2 border cursor-pointer text-left"
                onClick={() => handleSort("type")}
              >
                Job Type{renderSortArrow("type")}
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedJobs.map((job, index) => (
              <tr
                key={`${job.title}-${job.organization}-${index}`}
                className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}
              >
                <td className="px-4 py-2 border">
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-600 underline"
                  >
                    {job.title}
                  </a>
                </td>
                <td className="px-4 py-2 border">
                  {job.organization || "N/A"}
                </td>
                <td className="px-4 py-2 border">
                  {job.location || "N/A"}
                </td>
                <td className="px-4 py-2 border">
                  {job.type || "N/A"}
                </td>
              </tr>
            ))}

            {sortedJobs.length === 0 && (
              <tr>
                <td
                  colSpan={4}
                  className="px-4 py-4 border text-center text-gray-500"
                >
                  No jobs found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;

