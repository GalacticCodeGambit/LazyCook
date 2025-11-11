import { ChefHat, Search, BookOpen, Star, Clock, Smile } from 'lucide-react';
import { Button } from './components/ui/button';

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      {/* Top Bar */}
      <div className="bg-[#2c2c2c] text-white px-6 py-2 flex justify-between items-center">
        <span className="text-sm">Startseite</span>
        <div className="flex gap-1">
          <div className="w-4 h-4 border border-white/30 flex items-center justify-center text-xs">&lt;</div>
          <div className="w-4 h-4 border border-white/30 flex items-center justify-center text-xs">/</div>
          <div className="w-4 h-4 border border-white/30 flex items-center justify-center text-xs">&gt;</div>
        </div>
      </div>

      {/* Main Navigation */}
      <header className="border-b bg-white sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ChefHat className="w-8 h-8" />
            <span className="text-xl">Lazy Cook</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-6">
            <a href="#" className="text-gray-700 hover:text-black">Home</a>
            <a href="#" className="text-gray-700 hover:text-black">Recipe Finder</a>
            <a href="#" className="text-gray-700 hover:text-black">Impressum</a>
          </nav>

          <div className="flex items-center gap-3">
            <Button variant="ghost" className="text-sm">
              Anmelden
            </Button>
            <Button className="bg-black text-white hover:bg-black/90 text-sm rounded-md px-4">
              Registrieren
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-3xl mx-auto px-6 py-16 text-center">
        <div className="flex justify-center mb-6">
          <ChefHat className="w-20 h-20" strokeWidth={1.5} />
        </div>
        
        <h1 className="text-3xl mb-6">
          Finde perfekte Rezepte mit dem was du zu Hause hast
        </h1>
        
        <p className="text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
          Lassen Sie Ihre Zutaten nicht verderben! Geben Sie ein, was Sie in Ihrer Küche haben,
          und wir finden köstliche Rezepte, die Sie sofort zubereiten können. Kein Einkaufen
          erforderlich.
        </p>
        
        <Button className="bg-black text-white hover:bg-black/90 px-8 py-5 rounded-md">
          Kochen starten
        </Button>
      </section>

      {/* How it Works Section */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-center text-2xl mb-12">Funktionsweise</h2>
          
          <p className="text-center text-gray-700 mb-12 max-w-3xl mx-auto leading-relaxed">
            RecipeFinder erleichtert Ihnen das Kochen und hilft Ihnen, Rezepte mit Zutaten zu entdecken, die Sie bereits zu Hause
            haben. Geben Sie einfach Ihre verfügbaren Zutaten ein, und unsere intelligente Suche findet Hunderte köstlicher Rezepte.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-gray-200 w-16 h-16 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">1</span>
              </div>
              <h3 className="mb-3">Zutateneingabe</h3>
              <p className="text-gray-600 text-sm">
                Geben Sie ein, was Sie in Ihrer Küche haben – jede Zutat ist geeignet!
              </p>
            </div>

            <div className="text-center">
              <div className="bg-gray-200 w-16 h-16 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">2</span>
              </div>
              <h3 className="mb-3">Holen sie die Rezepte</h3>
              <p className="text-gray-600 text-sm">
                Unser Algorithmus findet Rezepte, die Ihre Zutaten verwenden.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-gray-200 w-16 h-16 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">3</span>
              </div>
              <h3 className="mb-3">Starte zu kochen</h3>
              <p className="text-gray-600 text-sm">
                Folgen Sie dem Rezept und genießen Sie Ihre köstliche Mahlzeit!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-center text-2xl mb-12">Eigenschaften</h2>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <Search className="w-12 h-12" strokeWidth={1.5} />
              </div>
              <h3 className="mb-3">Smart Suche</h3>
              <p className="text-gray-600 text-sm">
                Ein fortschrittlicher Algorithmus zur Zutatanabgleichung findet die besten Rezepte für Sie.
              </p>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-4">
                <BookOpen className="w-12 h-12" strokeWidth={1.5} />
              </div>
              <h3 className="mb-3">Detailed Instructions</h3>
              <p className="text-gray-600 text-sm">
                Dank der Schritt-für-Schritt-Kochanleitungen ist jedes Rezept leicht nachzukochen.
              </p>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-4">
                <Star className="w-12 h-12" strokeWidth={1.5} />
              </div>
              <h3 className="mb-3">Save Favorites</h3>
              <p className="text-gray-600 text-sm">
                Erstellen Sie ein Konto, um Ihre Lieblingsrezepte zu speichern und zu organisieren.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <ChefHat className="w-12 h-12" strokeWidth={1.5} />
              </div>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-4">
                <Clock className="w-12 h-12" strokeWidth={1.5} />
              </div>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-4">
                <Smile className="w-12 h-12" strokeWidth={1.5} />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}