import React, { useState, useEffect, useMemo } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [sortConfig, setSortConfig] = useState({
    key: "date_posted",
    direction: "desc",
  });
  const [query, setQuery] = useState("");

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

  // Enhanced normalization for YAF jobs
  function normalize(raw) {
    const title =
      raw.title ||
      raw.position ||
      raw.job_title ||
      raw.name ||
      raw.role ||
      "Untitled";

    const organization =
      raw.organization ||
      raw.org ||
      raw.company ||
      raw.employer ||
      raw.employer_name ||
      raw.institution ||
      "Unknown";

    const location =
      raw.location ||
      raw.job_location ||
      raw.city ||
      raw.jobCity ||
      raw.jobLocation ||
      raw["Job Location"] ||
      (raw.meta && raw.meta.location) ||
      "N/A";

    const type =
      raw.type ||
      raw.category ||
      raw.job_type ||
      raw.role_type ||
      raw.position_type ||
      raw.employment_type ||
      raw.categories ||
      (Array.isArray(raw.tags) ? raw.tags.join(", ") : undefined) ||
      (raw.meta && raw.meta.type) ||
      "N/A";

    const link =
      raw.link ||
      raw.url ||
      raw.apply_url ||
      raw.job_url ||
      raw.href ||
      (raw.meta && raw.meta.link) ||
      "#";

    // Date formats across YAF/TM variants
    const rawDate =
      raw.date_posted ||
      raw.date ||
      raw.posted ||
      raw.posted_at ||
      raw.post_date ||
      raw.published ||
      raw.publish_date ||
      (raw.meta && raw.meta.date) ||
      "";

    const date_posted = cleanDate(rawDate);

    return {
      title: String(title).trim(),
      organization: String(organization).trim(),
      location: String(location).trim(),
      type: String(type).trim(),
      date_posted,
      link: String(link).trim(),
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
    const mdy = /(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(value);
    if (mdy) {
      const [_, mo, da, yr] = mdy;
      const parsed = new Date(`${yr}-${mo}-${da}`);
      if (!isNaN(parsed)) return parsed.toISOString();
    }
    return value;
  }

  const filtered = useMemo(() => {
    if (!query) return jobs;
    const q = query.toLowerCase();
    return jobs.filter(
      (j) =>
        j.title.toLowerCase().includes(q) ||
        j.organization.toLowerCase().includes(q) ||
        j.location.toLowerCase().includes(q)
    );
  }, [jobs, query]);

  const sorted = useMemo(() => {
    const arr = [...filtered];
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
  }, [filtered, sortConfig]);

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

      {/* Search bar */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search jobs..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full md:w-1/2 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
        />
      </div>

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
            </tr>
          </thead>
          <tbody>
            {sorted.map((job, i) => (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="px-3 py-2 font-medium">
                  {job.link && job.link !== "#" ? (
                    <a
                      href={job.link}
                      target="_blank"
                      rel="noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {job.title}
                    </a>
                  ) : (
                    job.title
                  )}
                </td>
                <td className="px-3 py-2">{job.organization}</td>
                <td className="px-3 py-2">{job.location}</td>
                <td className="px-3 py-2">{job.type}</td>
                <td className="px-3 py-2">
                  {formatDate(job.date_posted)}
                </td>
              </tr>
            ))}
            {sorted.length === 0 && (
              <tr>
                <td
                  colSpan="5"
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

