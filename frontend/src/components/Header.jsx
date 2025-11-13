export default function Header() {
  return (
    <header className="bg-white border-b">
      <div className="max-w-6xl mx-auto px-4 py-5 flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">
          Conservative Jobs Board
        </h1>
        <div className="text-sm text-gray-500">
          Click column headers to sort
        </div>
      </div>
    </header>
  );
}

