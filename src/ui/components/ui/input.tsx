import { forwardRef } from 'react'
import { cn } from '../utils/cn'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<HTMLInputElement, InputProps>(({ className, ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        'flex h-11 w-full rounded-md border-2 border-input bg-background px-3 text-sm outline-none placeholder:text-muted-foreground/70 transition-all',
        'focus:border-primary focus:shadow-[0_0_0_4px] focus:shadow-primary/15',
        className
      )}
      {...props}
    />
  )
})
Input.displayName = 'Input'


