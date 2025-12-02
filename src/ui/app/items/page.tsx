import { Input } from '../../components/ui/input'
import { Badge } from '../../components/ui/badge'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader } from '../../components/ui/card'

export default function ItemsPage() {
  return (
    <section className="container mx-auto px-4 py-16 md:py-24">
      <div className="mb-6 grid grid-cols-1 gap-3 md:grid-cols-12">
        <div className="md:col-span-6">
          <Input placeholder="Filter agents, strategies, or datasets" />
        </div>
        <div className="md:col-span-6 flex flex-wrap items-center gap-2">
          {['Agents', 'Strategies', 'Datasets'].map((c) => (
            <Badge key={c} className="cursor-pointer transition-colors hover:bg-accent/70">{c}</Badge>
          ))}
          <Button variant="outline" className="ml-auto">Reset</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {[...Array(9)].map((_, i) => (
          <Card key={i} className="hover-elevate animate-in in-fade" style={{ animationDelay: `${80 * i}ms` }}>
            <CardHeader className="flex items-center justify-between pb-2">
              <div className="font-medium">{['Agent','Strategy','Dataset'][i % 3]} #{i + 1}</div>
              <Badge>{['Agents','Strategies','Datasets'][i % 3]}</Badge>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Explore configuration, metrics, and performance traces. Minimal CTA for demos only.
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}


