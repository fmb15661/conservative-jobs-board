import React, { useState, useEffect, useMemo } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [sortConfig, setSortConfig] = useState({
    key: "date_posted",
    direction: "desc",
  });

  useEffect(() => {
    async function loadJobs() {
      const sources = ["/jobs.json", "/jobs_yaf.json"];
      const allJobs = [];

      for (const src of sources) {
        try {
          const res = await fetch(src, { cache: "no-store" });
          if (!res.ok) continue;
          const data = await res.json();
          if (Array.isArray(data)) allJobs.push(...data);
        } catch {}
      }

      const normalized = allJobs.map((job) => normalize(job));
      setJobs(normalized);
    }

    loadJobs();
  }, []);

  function normalize(raw) {
    return {
      title: raw.title || raw.position || "Untitled",
      organization:
        raw.organization || raw.org || raw.company || "Unknown",
      location:
        raw.location || raw.job_location || raw.city || "N/A",
      type:
        raw.type || raw.category || raw.job_type || raw.role_type || "N/A",
      date_posted: cleanDate(
        raw.date_posted || raw.date || raw.posted || ""
      ),
      link: raw.link || raw.url || "#",
    };
  }

  function cleanDate(value) {
    if (!value) return "N/A";
    const d = new Date(value);
    if (!isNaN(d)) return d.toISOString();
    const match = /([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})/.exec(value);
    if (match) {
      const [_, m, day, y] = match;
      const parsed = new Date(`${m} ${day}, ${y}`);
      if (!isNaN(parsed)) return parsed.toISOString();
    }
    return value;
  }

  const sorted = useMemo(() => {
    const arr = [...jobs];
    const { key, direction } = sortConfig;
    const dir = direction === "asc" ? 1 : -1;

    arr.sort((a, b) => {
      if (key === "date_posted") {
        const ad = new Date(a.date_posted);
        const bd = new Date(b.date_posted);
        if (isNaN(ad) || isNaN(bd))
          return String(a.date_posted).localeCompare(
            String(b.date_posted)
          );
        return dir * (ad - bd);
      }
      return dir * String(a[key] || "").localeCompare(String(b[key] || ""));
    });
    return arr;
  }, [jobs, sortConfig]);

  function toggleSort(key) {
    setSortConfig((prev) => {
      if (prev.key === key) {
        return {
          key,
          direction: prev.direction === "asc" ? "desc" : "asc",
        };
      }
      return { key, direction: key === "date_posted" ? "desc" : "asc" };
    });
  }

  function arrow(key) {
    if (sortConfig.key !== key) return "↕";
    return sortConfig.direction === "asc" ? "↑" : "↓";
  }

  return (
    <div className="p-6 font-sans text-gray-900">
      <h1 className="text-2xl font-bold mb-4">
        Conservative Jobs Board
      </h1>
      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-gray-100">
            <tr>
              <th
                className="px-3 py-2 cursor-pointer"
                onClick={() => toggleSort("title")}
              >
                Title {arrow("title")}
              </th>
              <th
                className="px-3 py-2 cursor-pointer"
                onClick={() => toggleSort("organization")}
              >
                Organization {arrow("organization")}
              </th>
              <th
                className="px-3 py-2 cursor-pointer"
                onClick={() => toggleSort("location")}
              >
                Location {arrow("location")}
              </th>
              <th
                className="px-3 py-2 cursor-pointer"
                onClick={() => toggleSort("type")}
              >
                Type {arrow("type")}
              </th>
              <th
                className="px-3 py-2 cursor-pointer"
                onClick={() => toggleSort("date_posted")}
              >
                Date Posted {arrow("date_posted")}
              </th>
              <th className="px-3 py-2">Link</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((job, i) => (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="px-3 py-2 font-medium">{job.title}</td>
                <td className="px-3 py-2">{job.organization}</td>
                <td className="px-3 py-2">{job.location}</td>
                <td className="px-3 py-2">{job.type}</td>
                <td className="px-3 py-2">
                  {formatDate(job.date_posted)}
                </td>
                <td className="px-3 py-2">
                  {job.link && job.link !== "#" ? (
                    <a
                      href={job.link}
                      target="_blank"
                      rel="noreferrer"
                      className="text-blue-600 underline"
                    >
                      Apply
                    </a>
                  ) : (
                    "N/A"
                  )}
                </td>
              </tr>
            ))}
            {sorted.length === 0 && (
              <tr>
                <td
                  colSpan="6"
                  className="text-center py-6 text-gray-500"
                >
                  No jobs found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-gray-500 mt-2">
        Click any column header to sort ↑↓
      </p>
    </div>
  );

  function formatDate(value) {
    if (!value || value === "N/A") return "N/A";
    const d = new Date(value);
    if (isNaN(d)) return value;
    return d.toLocaleDateString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }
}

