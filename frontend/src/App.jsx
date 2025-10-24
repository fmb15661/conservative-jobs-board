import React, { useState, useEffect } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("/jobs.json")
      .then((res) => res.json())
      .then(setJobs)
      .catch(console.error);
  }, []);

  const filtered = jobs.filter((job) =>
    job.organization.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
        Conservative Jobs Board
      </h1>
      <input
        type="text"
        placeholder="Search organizations..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full p-2 mb-4 border rounded-lg shadow-sm"
      />
      <ul className="space-y-3">
        {filtered.map((org) => (
          <li key={org.organization} className="bg-white p-4 rounded-xl shadow">
            <h2 className="text-xl font-semibold">{org.organization}</h2>
            <a
              href={org.career_page}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              View Careers
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
