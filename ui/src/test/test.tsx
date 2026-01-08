import React, { useEffect, useRef } from 'react';
import {
  RocketLaunchIcon,
  CpuChipIcon,
  CircleStackIcon,
  CommandLineIcon,
  GlobeAltIcon,
  SparklesIcon,
  BoltIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline';

const TestPage: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const stars: { x: number; y: number; size: number; speed: number }[] = [];
    for (let i = 0; i < 200; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2,
        speed: Math.random() * 0.5 + 0.1,
      });
    }

    function animate() {
      if (!ctx || !canvas) return;
      ctx.fillStyle = 'rgba(3, 7, 18, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      stars.forEach((star) => {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fill();

        star.y += star.speed;
        if (star.y > canvas.height) {
          star.y = 0;
          star.x = Math.random() * canvas.width;
        }
      });

      requestAnimationFrame(animate);
    }

    animate();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className='relative min-h-screen bg-gradient-to-b from-slate-950 via-indigo-950 to-slate-900 text-white overflow-hidden'>
      {/* Animated Star Background */}
      <canvas ref={canvasRef} className='absolute inset-0 z-0' />

      {/* Cosmic Gradient Overlays */}
      <div className='absolute top-0 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl animate-pulse' />
      <div className='absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-600/20 rounded-full blur-3xl animate-pulse animation-delay-2000' />

      {/* Navigation */}
      <nav className='relative z-10 fixed w-full bg-slate-950/50 backdrop-blur-xl border-b border-cyan-500/20'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center h-16'>
            <div className='flex items-center gap-3'>
              <div className='w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/50'>
                <RocketLaunchIcon className='w-6 h-6 text-white' />
              </div>
              <span className='text-2xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent'>
                CosmicTech
              </span>
            </div>
            <div className='hidden md:flex items-center space-x-8'>
              <a
                href='#'
                className='text-cyan-300 hover:text-cyan-400 transition-colors font-medium'
              >
                Solutions
              </a>
              <a
                href='#'
                className='text-cyan-300 hover:text-cyan-400 transition-colors font-medium'
              >
                Technology
              </a>
              <a
                href='#'
                className='text-cyan-300 hover:text-cyan-400 transition-colors font-medium'
              >
                Mission
              </a>
              <button className='px-6 py-2 rounded-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all'>
                Launch App
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className='relative z-10 pt-32 pb-20 lg:pt-48 lg:pb-32'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center'>
          {/* Badge */}
          <div className='inline-flex items-center px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 mb-8 backdrop-blur-sm'>
            <SparklesIcon className='w-4 h-4 mr-2' />
            <span className='text-sm font-semibold'>Next-Gen Technology Platform</span>
          </div>

          {/* Main Heading */}
          <h1 className='text-6xl md:text-8xl font-extrabold tracking-tight mb-8 leading-tight'>
            <span className='block bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-gradient'>
              Explore the Digital
            </span>
            <span className='block text-white mt-2'>Universe</span>
          </h1>

          <p className='mt-6 max-w-3xl mx-auto text-xl text-cyan-100/80 mb-12 leading-relaxed'>
            Harness the power of cutting-edge technology and cosmic innovation. Build, deploy, and
            scale your applications across the digital cosmos with unprecedented speed and
            reliability.
          </p>

          {/* CTA Buttons */}
          <div className='flex flex-col sm:flex-row justify-center items-center gap-4 mb-16'>
            <button className='group w-full sm:w-auto px-8 py-4 rounded-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-bold text-lg hover:shadow-2xl hover:shadow-cyan-500/50 transition-all flex items-center justify-center'>
              <RocketLaunchIcon className='w-5 h-5 mr-2 group-hover:translate-y-[-4px] transition-transform' />
              Start Your Journey
            </button>
            <button className='w-full sm:w-auto px-8 py-4 rounded-full bg-white/5 backdrop-blur-sm text-cyan-300 font-bold text-lg border border-cyan-500/30 hover:bg-white/10 transition-all'>
              Explore Features
            </button>
          </div>

          {/* Stats */}
          <div className='grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto'>
            {[
              { value: '99.99%', label: 'Uptime' },
              { value: '< 10ms', label: 'Latency' },
              { value: '1M+', label: 'Deployments' },
              { value: '24/7', label: 'Support' },
            ].map((stat, i) => (
              <div
                key={i}
                className='p-4 rounded-xl bg-white/5 backdrop-blur-sm border border-cyan-500/20'
              >
                <div className='text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent'>
                  {stat.value}
                </div>
                <div className='text-cyan-300/60 text-sm mt-1'>{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className='relative z-10 py-24 bg-gradient-to-b from-transparent to-slate-950/50'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='text-center mb-16'>
            <h2 className='text-4xl md:text-5xl font-bold mb-4'>
              <span className='bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent'>
                Powered by Innovation
              </span>
            </h2>
            <p className='text-xl text-cyan-100/70 max-w-2xl mx-auto'>
              Advanced technology stack designed for the future of computing
            </p>
          </div>

          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
            {features.map((feature, index) => (
              <div
                key={index}
                className='group p-8 rounded-2xl bg-gradient-to-br from-cyan-500/10 to-purple-600/10 border border-cyan-500/20 hover:border-cyan-400/50 backdrop-blur-sm transition-all hover:scale-105 hover:shadow-2xl hover:shadow-cyan-500/20'
              >
                <div className='w-14 h-14 rounded-xl bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center mb-6 shadow-lg shadow-cyan-500/30 group-hover:scale-110 transition-transform'>
                  <feature.icon className='w-7 h-7 text-white' />
                </div>
                <h3 className='text-xl font-bold text-white mb-3 group-hover:text-cyan-400 transition-colors'>
                  {feature.title}
                </h3>
                <p className='text-cyan-100/60 leading-relaxed'>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tech Stack Section */}
      <div className='relative z-10 py-24 bg-slate-950/80 backdrop-blur-sm'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='text-center mb-16'>
            <h2 className='text-4xl md:text-5xl font-bold mb-4 text-white'>
              Enterprise-Grade Infrastructure
            </h2>
            <p className='text-xl text-cyan-100/70'>Built on the most reliable technology stack</p>
          </div>

          <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6'>
            {['Node.js', 'React', 'TypeScript', 'Docker', 'Kubernetes', 'PostgreSQL'].map(
              (tech) => (
                <div
                  key={tech}
                  className='p-6 rounded-xl bg-gradient-to-br from-cyan-500/5 to-purple-600/5 border border-cyan-500/20 hover:border-cyan-400/50 backdrop-blur-sm text-center transition-all hover:scale-110 hover:shadow-lg hover:shadow-cyan-500/20'
                >
                  <div className='text-lg font-bold text-cyan-300'>{tech}</div>
                </div>
              )
            )}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className='relative z-10 py-24 overflow-hidden'>
        <div className='absolute inset-0 bg-gradient-to-r from-cyan-600/20 to-purple-600/20 blur-3xl' />
        <div className='max-w-4xl mx-auto px-4 text-center relative'>
          <h2 className='text-4xl md:text-6xl font-bold mb-6'>
            <span className='bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent'>
              Ready to Launch?
            </span>
          </h2>
          <p className='text-xl text-cyan-100/80 mb-10 max-w-2xl mx-auto'>
            Join thousands of developers building the future with CosmicTech
          </p>
          <button className='group px-12 py-5 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-full font-bold text-xl shadow-2xl shadow-cyan-500/50 hover:shadow-cyan-500/70 transition-all transform hover:scale-105'>
            <span className='flex items-center'>
              Start Building Now
              <RocketLaunchIcon className='w-6 h-6 ml-2 group-hover:translate-x-2 transition-transform' />
            </span>
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className='relative z-10 bg-slate-950/90 backdrop-blur-sm border-t border-cyan-500/20 pt-16 pb-8'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='grid grid-cols-2 md:grid-cols-4 gap-8 mb-12'>
            <div className='col-span-2'>
              <div className='flex items-center gap-3 mb-4'>
                <div className='w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center'>
                  <RocketLaunchIcon className='w-6 h-6 text-white' />
                </div>
                <span className='text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent'>
                  CosmicTech
                </span>
              </div>
              <p className='text-cyan-100/60 max-w-xs mb-6'>
                Building the future of technology, one innovation at a time.
              </p>
            </div>

            {[
              { title: 'Product', links: ['Features', 'Pricing', 'Security', 'Roadmap'] },
              { title: 'Company', links: ['About', 'Blog', 'Careers', 'Contact'] },
            ].map((section) => (
              <div key={section.title}>
                <h4 className='font-bold text-white mb-4'>{section.title}</h4>
                <ul className='space-y-2'>
                  {section.links.map((link) => (
                    <li key={link}>
                      <a
                        href='#'
                        className='text-cyan-100/60 hover:text-cyan-400 transition-colors'
                      >
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className='pt-8 border-t border-cyan-500/20 text-center text-cyan-100/50 text-sm'>
            © {new Date().getFullYear()} CosmicTech. All rights reserved.
          </div>
        </div>
      </footer>

      <style>{`
        @keyframes gradient {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
      `}</style>
    </div>
  );
};

const features = [
  {
    title: 'Quantum Computing',
    description: 'Leverage quantum algorithms for unprecedented computational power.',
    icon: CpuChipIcon,
  },
  {
    title: 'Neural Networks',
    description: 'AI-powered systems that learn and adapt to your needs.',
    icon: CommandLineIcon,
  },
  {
    title: 'Cloud Infrastructure',
    description: 'Distributed systems spanning the digital cosmos.',
    icon: GlobeAltIcon,
  },
  {
    title: 'Data Security',
    description: 'Military-grade encryption protecting your universe.',
    icon: ShieldCheckIcon,
  },
  {
    title: 'Real-time Sync',
    description: 'Instant synchronization across all dimensions.',
    icon: BoltIcon,
  },
  {
    title: 'Scalable Storage',
    description: 'Infinite storage capacity that grows with you.',
    icon: CircleStackIcon,
  },
  {
    title: 'Auto-scaling',
    description: 'Automatically adapt to cosmic-scale demands.',
    icon: SparklesIcon,
  },
  {
    title: 'Mission Control',
    description: 'Command center for all your operations.',
    icon: RocketLaunchIcon,
  },
];

export default TestPage;
