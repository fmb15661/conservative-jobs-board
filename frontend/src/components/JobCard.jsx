export default function JobCard({ job }) {
  // Safeguards (already normalized in App.jsx, but keep this defensive)
  const title = job.title || "Untitled";
  const organization = job.organization || "Unknown";
  const location = job.location || "N/A";
  const type = job.type || "N/A";
  const link = job.link && job.link !== "#" ? job.link : null;

  // Show a human-friendly date:
  // If ISO string, format as "Mon DD, YYYY"; otherwise show as-is or "N/A".
  let dateDisplay = "N/A";
  if (job.date_posted) {
    if (/^\d{4}-\d{2}-\d{2}T/.test(job.date_posted)) {
      const d = new Date(job.date_posted);
      if (!isNaN(d.getTime())) {
        dateDisplay = d.toLocaleDateString(undefined, {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
      } else {
        dateDisplay = String(job.date_posted);
      }
    } else {
      dateDisplay = String(job.date_posted);
    }
  }

  return (
    <tr className="border-b last:border-none hover:bg-gray-50">
      <td className="px-4 py-3 font-medium">{title}</td>
      <td className="px-4 py-3">{organization}</td>
      <td className="px-4 py-3">{location}</td>
      <td className="px-4 py-3">{type}</td>
      <td className="px-4 py-3">{dateDisplay}</td>
      <td className="px-4 py-3">
        {link ? (
          <a
            href={link}
            target="_blank"
            rel="noreferrer"
            className="inline-block px-3 py-1 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
          >
            Apply
          </a>
        ) : (
          <span className="text-gray-400">N/A</span>
        )}
      </td>
    </tr>
  );
}

