import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadJobs() {
      try {
        const res1 = await fetch("/jobs.json");
        const res2 = await fetch("/jobs_talentmarket.json");

        const d1 = await res1.json();
        const d2 = await res2.json();

        const combined = [...d1, ...d2].map((j) => ({
          title: String(j.title || ""),
          organization: String(j.organization || ""),
          location: typeof j.location === "object"
            ? `${j.location.city || ""}, ${j.location.state || ""}`
            : String(j.location || ""),
          type: String(j.type || ""),
          date_posted: String(j.date_posted || ""),
          link: String(j.link || "#"),
        }));

        combined.sort((a, b) => new Date(b.date_posted) - new Date(a.date_posted));

        setJobs(combined);
      } catch (e) {
        console.error("loadJobs error:", e);
      }
    }
    loadJobs();
  }, []);

  const filtered = jobs.filter((j) =>
    j.title.toLowerCase().includes(search.toLowerCase()) ||
    j.organization.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Conservative Jobs Board</h1>

      <input
        type="text"
        placeholder="Search job titles or organizations..."
        className="w-full border rounded-lg p-2 mb-6"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-4 py-2 text-left">Job Title</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Organization</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Location</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Date Posted</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((job, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-4 py-2">
                  <a href={job.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    {job.title}
                  </a>
                </td>
                <td className="border border-gray-300 px-4 py-2">{job.organization}</td>
                <td className="border border-gray-300 px-4 py-2">{job.location}</td>
                <td className="border border-gray-300 px-4 py-2">{job.date_posted}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
