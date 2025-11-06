import { useEffect, useState } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function go() {
      const r = await fetch("/jobs.json");
      const data = await r.json();
      setJobs(data);
    }
    go();
  }, []);

  const filtered = jobs.filter((j) =>
    (j.title + j.organization + j.location)
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-6">
          Conservative Jobs Board
        </h1>

        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search jobs..."
          className="w-full p-2 border border-gray-300 rounded-lg mb-6"
        />

        <div className="overflow-x-auto">
          <table className="table w-full border-collapse">
            <thead>
              <tr className="bg-white">
                <th className="text-left p-2 border border-gray-300">Title</th>
                <th className="text-left p-2 border border-gray-300">Organization</th>
                <th className="text-left p-2 border border-gray-300">Job Type</th>
                <th className="text-left p-2 border border-gray-300">Location</th>
                <th className="text-left p-2 border border-gray-300">Date Posted</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((j, i) => (
                <tr key={i} className="bg-white hover:bg-gray-50">
                  <td className="p-2 border border-gray-300">
                    <a className="text-blue-600 hover:underline" target="_blank" href={j.link}>
                      {j.title}
                    </a>
                  </td>
                  <td className="p-2 border border-gray-300">{j.organization}</td>
                  <td className="p-2 border border-gray-300">{j["Job Type"] || ""}</td>
                  <td className="p-2 border border-gray-300">{j.location}</td>
                  <td className="p-2 border border-gray-300">{j.date_posted}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
