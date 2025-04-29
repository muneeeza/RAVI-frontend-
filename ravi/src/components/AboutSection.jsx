import React from 'react';
import step1Image from '../assets/step1.jpg';
import step2Image from '../assets/step2.jpg';
import step3Image from '../assets/step3.jpg';
import { useTranslation } from 'react-i18next';


const HowItWorks = () => {
  const { t } = useTranslation();
  return (
    <section id="how-it-works" className="py-20 bg-gradient-to-b from-[#f6f7f4] to-[#eef0ea] text-center">
      {/* Section Title */}
      <h2 className="text-5xl font-josefin font-semibold mb-8 text-body_text font-sans rtl:font-urdu ltr:font-quicksand">
        {t('aboutSection.part1')}
        <span className="text-highlight_color">
          {t('aboutSection.part2')}
        </span>
        {t('aboutSection.part3')}
      </h2>
      <p className="text-lg font-medium mb-12 text-body_text max-w-3xl mx-auto font-quicksand rtl:font-urdu ltr:font-quicksand">
        {t('aboutSection.content')}
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-12 max-w-7xl mx-auto px-1">
        {/* Step 1 */}
        <div className="flex flex-col items-center bg-gray-50 p-6 rounded-xl shadow-md border-t-4 border-p_1 hover:shadow-xl hover:scale-105 transition-transform duration-300 ease-in-out">
          <div className="flex items-center justify-center bg-p_2 text-p_1 rounded-full h-12 w-12 mb-4 text-xl font-bold">1</div>
          <img src={step1Image} alt="Upload an Image" className="h-48 w-full mb-6 rounded-lg object-cover transition-transform duration-500 ease-in-out transform hover:scale-105" />
          <h3 className="text-2xl font-josefin font-semibold mb-2 text-main_text rtl:font-urdu ltr:font-quicksand">{t('aboutSection.box1_Title')}</h3>
          <p className="text-body_text text-base rtl:font-urdu ltr:font-quicksand">{t('aboutSection.box1_Content')}</p>
        </div>

        {/* Step 2 */}
        <div className="flex flex-col items-center bg-bg_color p-6 rounded-xl shadow-md border-t-4 border-p_1 hover:shadow-xl hover:scale-105 transition-transform duration-300 ease-in-out">
          <div className="flex items-center justify-center bg-p_2 text-p_1 rounded-full h-12 w-12 mb-4 text-xl font-bold">2</div>
          <img src={step2Image} alt="AI processes the image to audio!" className="h-48 w-full mb-6 rounded-lg object-cover transition-transform duration-500 ease-in-out transform hover:scale-105" />
          <h3 className="text-2xl font-josefin font-semibold mb-2 text-main_text rtl:font-urdu ltr:font-quicksand ">{t('aboutSection.box2_Title')}</h3>
          <p className="text-body_text text-base rtl:font-urdu ltr:font-quicksand">{t('aboutSection.box2_Content')}</p>
        </div>

        {/* Step 3 */}
        <div className="flex flex-col items-center bg-bg_color p-6 rounded-xl shadow-md border-t-4 border-p_1 hover:shadow-xl hover:scale-105 transition-transform duration-300 ease-in-out">
          <div className="flex items-center justify-center bg-p_2 text-p_1 rounded-full h-12 w-12 mb-4 text-xl font-bold">3</div>
          <img src={step3Image} alt="The audio is played" className="h-48 w-full mb-6 rounded-lg object-cover transition-transform duration-500 ease-in-out transform hover:scale-105" />
          <h3 className="text-2xl font-josefin font-semibold mb-2 text-main_text rtl:font-urdu ltr:font-quicksand ">{t('aboutSection.box3_Title')}</h3>
          <p className="text-body_text text-base rtl:font-urdu ltr:font-quicksand">{t('aboutSection.box3_Content')}</p>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
