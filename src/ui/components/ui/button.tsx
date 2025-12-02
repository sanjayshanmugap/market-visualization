import { forwardRef } from 'react'
import { cn } from '../utils/cn'

type Variant = 'default' | 'outline' | 'secondary' | 'ghost'
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  asChild?: boolean
}

const base =
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-all active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50'

const variants: Record<Variant, string> = {
  default:
    'gradient-primary text-white shadow-sm border border-transparent hover:opacity-90 px-4 py-2',
  outline:
    'border-2 border-border bg-background text-foreground hover:border-primary/50 hover:shadow-md px-4 py-2',
  secondary:
    'bg-success text-success-foreground border border-border hover:opacity-90 px-4 py-2',
  ghost:
    'bg-transparent text-foreground hover:bg-accent/40 border border-transparent px-3 py-2',
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return <button ref={ref} className={cn(base, variants[variant], className)} {...props} />
  }
)
Button.displayName = 'Button'


