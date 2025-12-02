import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'

const techStack = {
  python: [
    'matplotlib',
    'seaborn',
    'plotly',
    'bokeh',
    'altair',
    'folium',
    'networkx',
    'pandas',
    'numpy',
  ],
  frontend: [
    'Next.js 14',
    'React',
    'TypeScript',
    'Tailwind CSS',
    'D3.js',
    'react-plotly.js',
    'Three.js',
    'Leaflet',
  ],
  backend: ['FastAPI', 'Python', 'Uvicorn'],
}

const domains = [
  { name: 'Financial', description: 'Stock market analysis, correlation networks, trading patterns' },
  { name: 'Climate', description: 'Temperature trends, climate change impact, weather events' },
  { name: 'Social/Economic', description: 'Economic inequality, population dynamics, social trends' },
  { name: 'Scientific', description: 'Paper networks, tool ecosystems, 3D data exploration' },
]

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="mb-12">
        <h1 className="text-4xl font-bold mb-4">About This Portfolio</h1>
        <p className="text-lg text-muted-foreground">
          This data visualization portfolio showcases technical skills in Python visualization libraries,
          data storytelling, and visual design across multiple domains and formats.
        </p>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Tech Stack</h2>
        <div className="grid gap-6 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Python Libraries</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {techStack.python.map((lib) => (
                  <Badge key={lib} variant="secondary">
                    {lib}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Frontend</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {techStack.frontend.map((tech) => (
                  <Badge key={tech} variant="outline">
                    {tech}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Backend</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {techStack.backend.map((tech) => (
                  <Badge key={tech} variant="outline">
                    {tech}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Visualization Domains</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {domains.map((domain) => (
            <Card key={domain.name}>
              <CardHeader>
                <CardTitle>{domain.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{domain.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Methodology</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">1. Data Collection</h3>
                <p className="text-muted-foreground">
                  Data is collected from public APIs and datasets across multiple domains, ensuring
                  diverse and interesting datasets for visualization.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">2. Python Generation</h3>
                <p className="text-muted-foreground">
                  All visualizations are generated using Python libraries, taking advantage of the
                  rich ecosystem of visualization tools available.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">3. Export & Integration</h3>
                <p className="text-muted-foreground">
                  Visualizations are exported in appropriate formats (static images, JSON for interactive
                  charts) and integrated into the Next.js frontend.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">4. Storytelling</h3>
                <p className="text-muted-foreground">
                  Each visualization is presented with narrative context, explaining the data story
                  and key insights.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}

