import { forwardRef } from 'react'
import { cn } from '../utils/cn'

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={cn(
          'min-h-[120px] w-full resize-none rounded-md border-2 border-input bg-background p-3 text-sm outline-none placeholder:text-muted-foreground/70 transition-all',
          'focus:border-primary focus:shadow-[0_0_0_4px] focus:shadow-primary/15',
          className
        )}
        {...props}
      />
    )
  }
)
Textarea.displayName = 'Textarea'


