kimport React, { useState, useEffect, useMemo } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: "title", direction: "asc" });
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
        } catch (e) {
          console.error("Failed to load", src, e);
        }
      }

      const normalized = allJobs.map(normalize);
      const seen = new Set();
      const unique = [];

      for (const job of normalized) {
        const key =
          (job.link && job.link !== "#"
            ? job.link
            : `${job.title}-${job.organization}`).toLowerCase();
        if (!seen.has(key)) {
          seen.add(key);
          unique.push(job);
        }
      }
      setJobs(unique);
    }

    loadJobs();
  }, []);

  function normalize(raw) {
    return {
      title: raw.title || raw.position || "Untitled",
      organization:
        raw.organization ||
        raw.org ||
        raw.company ||
        raw.employer ||
        "Unknown",
      location:
        raw.location ||
        raw.job_location ||
        raw.city ||
        raw.jobCity ||
        raw.jobLocation ||
        raw["Job Location"] ||
        "N/A",
      type:
        raw.type ||
        raw.category ||
        raw.job_type ||
        raw.role_type ||
        raw.position_type ||
        raw.employment_type ||
        raw.categories ||
        "N/A",
      link: raw.link || raw.url || "#",
    };
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
    arr.sort((a, b) =>
      dir * String(a[key] || "").localeCompare(String(b[key] || ""))
    );
    return arr;
  }, [filtered, sortConfig]);

  function toggleSort(key) {
    setSortConfig((prev) => {
      if (prev.key === key) {
        return { key, direction: prev.direction === "asc" ? "desc" : "asc" };
      }
      return { key, direction: "asc" };
    });
  }

  function arrow(key) {
    if (sortConfig.key !== key) return "↕";
    return sortConfig.direction === "asc" ? "↑" : "↓";
  }

  return (
    <div className="p-6 font-sans text-gray-900">
      <h1 className="text-2xl font-bold mb-4">Conservative Jobs Board</h1>

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

      {/* Jobs table */}
      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-3 py-2 cursor-pointer" onClick={() => toggleSort("title")}>
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
              <th className="px-3 py-2 cursor-pointer" onClick={() => toggleSort("type")}>
                Type {arrow("type")}
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
              </tr>
            ))}
            {sorted.length === 0 && (
              <tr>
                <td colSpan="4" className="text-center py-6 text-gray-500">
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
}

